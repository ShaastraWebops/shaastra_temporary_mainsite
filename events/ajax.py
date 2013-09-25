# For simple dajax(ice) functionalities
from django.utils import simplejson
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string
# From shaasta_mainsite_2014
from mainsite_2014.settings import MEDIA_ROOT, DATABASES
# Python imports
import json
import os

def get_json_file_path(filename):
    file_path = os.path.abspath( os.path.join( MEDIA_ROOT, 'json', 'events') )
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return os.path.join(file_path, filename)
    
@dajaxice_register
def show_event(request, event_name=None):
    '''
        Gets the data for the requested event from the JSON file and renders it.
        
        args-
            event_name: holds the name of the event that throwed the request
        
        vars-
            json_dict: holds the data retrieved from the event json file
            erp_db: holds the database alias of the erp database
    '''
    dajax = Dajax()
    json_dict = {}
    event_instance = None
    
    #version1 : event_name gives the json_file name
    if not event_name:
        show_alert(dajax, "error", "There is some error on the site, please report to WebOps team")
        return dajax.json()
    
    event_json_filepath = get_json_file_path( str(event_name) )
    if not os.path.exists(event_json_filepath):
        show_alert(dajax, "error", "There is some error on the site, please report to WebOps team")
        return dajax.json()
    else:
        with open(event_json_filepath) as f:
            json_dict = json.dumps(json.load(f), sort_keys=False, indent=4) # This is a json object
            html_content = render_to_string('events/'+ 'test_event' +'.html', locals(), RequestContext(request))
            f.close()
    if html_content:
        dajax.assign('#'+event_name, 'innerHTML', html_content)
    
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
