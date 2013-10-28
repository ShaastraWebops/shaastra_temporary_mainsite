# For simple dajax(ice) functionalities
from django.utils import simplejson
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string
# From shaasta_mainsite_2014
from mainsite_2014.settings import ERP_PROJECT_PATH, DATABASES
from models import ParticipantEvent
erp_db = DATABASES.keys()[1]
from django.utils import timezone
# Python imports
import json
import os,datetime

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
    update_details = {}
    update_details_list = []
    
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
    
    #getting event, tab and update data separately from json_dict
    tab_pk_list = []
    update_pk_list = []
    skip_update_pk = []
    json_dict_keys = sorted(json_dict) # sorted keys
    tab_count = 1
    update_count = 1
    
    for key in json_dict_keys:
        if key.startswith('event_'):
            event_details[ key[6:] ] = json_dict.pop(key)
            
        elif key.startswith('tab'):
            tab_underscore_posn = key.find('_')
            tab_pk = key[3:tab_underscore_posn]
            if tab_count==1:
                tab_details[ key[tab_underscore_posn+1:] ] = json_dict.pop(key)
            elif ( int(tab_pk) == int(tab_pk_list[-1]) ) and (tab_count>1) :
                tab_details[ key[tab_underscore_posn+1:] ] = json_dict.pop(key)
            elif ( int(tab_pk) != int(tab_pk_list[-1]) ) and (tab_count>1) :
                tab_details_list.append(tab_details)
                tab_details = {}
                tab_details[ key[tab_underscore_posn+1:] ] = json_dict.pop(key)

            tab_pk_list.append(tab_pk)
            tab_count += 1
            
        elif key.startswith('update'):
            update_underscore_posn = key.find('_')
            update_pk = key[6:update_underscore_posn]
#            if key[update_underscore_posn+1:] == 'expired' and json_dict[key] == True:
#                skip_update_pk.append(update_pk)
#                continue
            if update_count==1:
                update_details[ key[update_underscore_posn+1:] ] = json_dict.pop(key)
            elif ( int(update_pk) == int(update_pk_list[-1]) ) and (update_count>1) :
                update_details[ key[update_underscore_posn+1:] ] = json_dict.pop(key)
            elif ( int(update_pk) != int(update_pk_list[-1]) ) and (update_count>1) :
                update_details_list.append(update_details)
                update_details = {}
                update_details[ key[update_underscore_posn+1:] ] = json_dict.pop(key)

            update_pk_list.append(update_pk)
            update_count += 1

    if tab_details:
        tab_details_list.append(tab_details) #appending the last tab_details dict that was not appended in the loop
        
    if update_details:
        update_details_list.append(update_details) #appending the last update_details dict that was not appended in the loop
    
    # removing expired updates from updates list
    for update_details in update_details_list:
        if update_details['expired'] == True:
            update_details_list.remove(update_details)
    
    #sorting tab details based on preference:
    tab_details_list = sorted(tab_details_list, key=lambda x: x["pref"])
    update_details_list = sorted(update_details_list, key=lambda x: x["category"])
    time_now = timezone.now()
    context_dict = {'event' : event_details, 'tab_list': tab_details_list, 'updates_list': update_details_list, 'event_type': event_type, 'time_now':time_now, 'event_pk':event_pk}
    html_content = render_to_string('events/small/event_page.html', context_dict, RequestContext(request))
    
    if html_content:
        dajax.script("window.location.hash='"+ event_name.replace(" ","_").lower() +"'")
        dajax.assign("#event_no_"+str(event_pk)+" > .event_content", "innerHTML", html_content)
        #dajax.script("show_event(document.getElementById('event_no_"+str(event_pk)+"_click'));")
        dajax.script("$('#event_no_"+str(event_pk)+"_click').parent().children('.event_content').removeClass('loading');")
    return dajax.json() 
