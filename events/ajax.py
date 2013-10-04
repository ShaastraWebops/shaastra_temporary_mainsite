# For simple dajax(ice) functionalities
from django.utils import simplejson
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string
# From shaasta_mainsite_2014
from mainsite_2014.settings import ERP_PROJECT_PATH, DATABASES
# Python imports
import json
import os

def get_json_file_path(filename):
    file_path = os.path.abspath( os.path.join( ERP_PROJECT_PATH, 'media', 'json', 'events') )
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return os.path.join(file_path, filename)
    
@dajaxice_register
def show_event(request, event_pk=None, event_name=None, event_type=None):
    '''
        Gets the data for the requested event from the JSON file and renders it.
        
        args-
            event_pk: holds the pk of the event that throwed the request
            event_name: holds the name of the event that throwed the request
            event_type: holds the type of the event (Participant or Audience)
        vars-
            json_dict: holds the data retrieved from the event json file
            erp_db: holds the database alias of the erp database
            event_details: holds events details part of json_dict
            tab_details_list: holds tab details for each tab in json_dict
    '''
    dajax = Dajax()
    json_dict = {}
    event_details = {}
    tab_details = {}
    tab_details_list = []
    
    if not (event_pk and event_name):
        dajax.script('$.bootstrapGrowl("Oops : There is some error on the site, please report to WebOps team", {type:"danger"} );' )
        return dajax.json()
        
    try:
        event_pk = int(event_pk)
    except:
        dajax.script('$.bootstrapGrowl("Oops : There is some error on the site, please report to WebOps team.", {type:"danger"} );' )
        return dajax.json()
    
    event_name = event_name.replace("~", " ")
    
    event_json_filepath = get_json_file_path( str(event_pk) + "_" + event_name +".json" )
    print event_json_filepath
    if not os.path.exists(event_json_filepath):
        dajax.script('$.bootstrapGrowl("Oops : There is some error on the site, please report to WebOps team..", {type:"danger"} );' )
        return dajax.json()
    else:
        with open(event_json_filepath) as f:
            json_dict = json.load(f)
            f.close()
    
    #getting event and tab data separately from json_dict
    tab_pk_list = []
    json_dict_keys = sorted(json_dict) # sorted keys
    count=1
    
    for key in json_dict_keys:
        if key.startswith('event_'):
            event_details[ key[6:] ] = json_dict.pop(key)
        else:
            underscore_posn = key.find('_')
            tab_pk = key[3:underscore_posn]
            if count==1:
                tab_details[ key[underscore_posn+1:] ] = json_dict.pop(key)
            elif ( int(tab_pk) == int(tab_pk_list[-1]) ) and (count>1) :
                tab_details[ key[underscore_posn+1:] ] = json_dict.pop(key)
            elif ( int(tab_pk) != int(tab_pk_list[-1]) ) and (count>1) :
                tab_details_list.append(tab_details)
                tab_details = {}
                tab_details[ key[underscore_posn+1:] ] = json_dict.pop(key)

            tab_pk_list.append(tab_pk)
            count += 1
    
    if tab_details:        
        tab_details_list.append(tab_details) #appending the last tab_details dict that was not appended in the loop
    
    #sorting tab details based on preference:
    tab_details_list = sorted(tab_details_list, key=lambda x: x["pref"])
        
    context_dict = {'event' : event_details, 'tab_list': tab_details_list, 'event_type': event_type }
    html_content = render_to_string('events/small/event_page.html', context_dict, RequestContext(request))
    
    if html_content:
        dajax.assign("#event_no_"+str(event_pk)+" > .event_content", "innerHTML", html_content)
        #dajax.script("show_event(document.getElementById('event_no_"+str(event_pk)+"_click'));")
        dajax.script("$('#event_no_"+str(event_pk)+"_click').parent().children('.event_content').removeClass('loading');")
    
    return dajax.json()
