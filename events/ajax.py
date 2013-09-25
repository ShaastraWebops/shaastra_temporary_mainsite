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
def show_event(request, event_pk=None, event_name=None):
    '''
        Gets the data for the requested event from the JSON file and renders it.
        
        args-
            event_pk: holds the pk of the event that throwed the request
            event_name: holds the name of the event that throwed the request
        vars-
            json_dict: holds the data retrieved from the event json file
            erp_db: holds the database alias of the erp database
    '''
    dajax = Dajax()
    json_dict = {}
    event_details = {}
    tab_details = {}
    tab_details_list = []
    
    if not (event_pk or event_type):
        dajax.script('$.bootstrapGrowl("Oops : There is some error on the site, please report to WebOps team.", {type:"danger"} );' )
        return dajax.json()
        
    try:
        event_pk = int(event_pk)
    except:
        dajax.script('$.bootstrapGrowl("Oops : There is some error on the site, please report to WebOps team.", {type:"danger"} );' )
        return dajax.json()
    
    event_json_filepath = get_json_file_path( str(event_pk) + "_" + event_name +".json" )
    print event_json_filepath
    if not os.path.exists(event_json_filepath):
        dajax.script('$.bootstrapGrowl("Oops : There is some error on the site, please report to WebOps team.", {type:"danger"} );' )
        return dajax.json()
    else:
        with open(event_json_filepath) as f:
            json_dict = json.load(f)
            f.close()
    
    #getting number of tabs present
    tab_pk_list = []
#    for key in json_dict.keys():
#        if key.startswith('tab'):
#            underscore_posn = key.find('_')
#            tab_pk = str(key[3:underscore_posn])
#            if not (tab_pk in tab_pk_list):
#                tab_pk_list.append( tab_pk )
#    
#    #getting event and tab data separately from json_dict
#    for key in json_dict.keys():
#        if key.startswith('event_'):
#            event_details[ key[6:] ] = json_dict.pop(key)
#        else:
#                tab_pk_list.append( tab_pk )
#            start_posn = key.find('_') + 1
#            tab_details[ key[start_posn:] ] = json_dict[key]
#            tab_details_list.append(tab_details)

    json_dict_keys = sorted(json_dict) # sorted keys
    count=1
    

            
    context_dict = {'event' : event_details, 'tab_list': tab_details_list }
    html_content = render_to_string('events/small/event_page.html', context_dict, RequestContext(request))
    
    if html_content:
        dajax.assign("#event_no_"+str(event_pk)+" > .event_content", "innerHTML", html_content)
        dajax.script("$el = document.getElementById('event_no_"+str(event_pk)+"_click');\
                      show_event($el);")
#        dajax.script("$('#event_no_"+str(event_pk)+"').find('.event_content').html('"+html_content+"');")
    
    return dajax.json()
    
    #version2 : event_name is given, querry the db and get the json filename
    '''erp_db = DATABASES.keys()[1] # the second key in DATABASES dict in settings.py corresponds to erp db
    if not event_name:
        show_alert(dajax, "error", "There is some error on the site, please report to WebOps team")
        return dajax.json()
    else:
        event_instance = GenericEvent.objects.using(erp_db).filter(title=event_name)[0]
        event_pk = event_instance.pk
    
    event_json_filepath = get_json_file_path( str(event_pk) + "_" + event_name )
    if not os.path.exists(event_json_filepath):
        show_alert(dajax, "error", "There is some error on the site, please report to WebOps team")
        return dajax.json()
    else:
        with open(event_json_filepath) as f:
            json_dict = json.dumps(json.load(f), sort_keys=False, indent=4) # This is a json object
            html_content = render_to_string('events/'+ 'test_event' +'.html', locals(), RequestContext(request))
            f.close()
    
    if html_content:
        dajax.assign()'''
