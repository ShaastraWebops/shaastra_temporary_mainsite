# For simple dajax(ice) functionalities
from django.utils import simplejson
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string
# From shaasta_mainsite_2014
from mainsite_2014.settings import ERP_PROJECT_PATH, DATABASES
from events.models import ParticipantEvent, Event_html_dump
erp_db = DATABASES.keys()[1]
from django.utils import timezone
# Python imports
import json
import os, datetime, glob

#tuple relating events to spons logos
EVENT_SPONS = ({"Research Confluence": ["hindu.png","knimbus.png"]}, {"Estimus": ["musigma.png"]}, {"Triathlon": ["vmware.jpg"]},\
                    {"Robowars": ["eaton.jpg"]}, {"Shaastra Cube Open": ["vmware.jpg"]}, {"How Things Work": ["lincpens.png"]},\
                    {"Master Builder": ["nrdave.png"]}, {"GE Industry Defined Problem": ["ge.jpg"]},\
                    {"Eaton Industry Defined Problem": ["eaton.jpg"]}, {"Ericsson Industry Defined Problem": ["ericsson.tif"]},\
                    {"Paper and Poster Presentation": ["tcs.jpg"]})

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
    
    if not Event_html_dump.objects.all().count():
        json_dir_path = os.path.abspath( os.path.join( ERP_PROJECT_PATH, 'media', 'json', 'events') )
        json_filepaths = glob.glob(json_dir_path + '/*.json')
        
        for event_json_filepath in json_filepaths:
            try:
                create_html_dump(len(json_dir_path)+1, event_json_filepath)
            except:
                continue
    
    event_name = event_name.replace("~", " ")

    event_json_filepath = get_json_file_path( str(event_pk) + "_" + event_name +".json" )

    if not os.path.exists(event_json_filepath):
        dajax.script('$.bootstrapGrowl("Oops : There is some error on the site, please report to WebOps team..", {type:"danger"} );' )
        return dajax.json()
    else:
        try:
            event_dump = Event_html_dump.objects.get(event_pk = event_pk)
        except:
            json_dir_path = os.path.abspath( os.path.join( ERP_PROJECT_PATH, 'media', 'json', 'events') )
            create_html_dump(len(json_dir_path)+1, event_json_filepath)
            event_dump = Event_html_dump.objects.get(event_pk = event_pk)
        
    html_content = event_dump.html_content
        
    if html_content:
        dajax.script("window.location.hash='"+ event_name.replace(" ","_").lower() +"'")
        dajax.assign("#event_no_"+str(event_pk)+" > .event_content", "innerHTML", html_content)
        #dajax.script("show_event(document.getElementById('event_no_"+str(event_pk)+"_click'));")
        dajax.script("$('#event_no_"+str(event_pk)+"_click').parent().children('.event_content').removeClass('loading');")
        dajax.script('setTimeout( function() {$("#modal_update_event").css({"width" : ( $("body").width() - ( $("#modal_update_event").parent().children(".page_content").offset().left + $("#modal_update_event").parent().children(".page_content").width() ) - 50 ) +"px",})}, 100);')
    return dajax.json() 
    
def create_html_dump(event_name_start_posn, event_json_filepath):
    '''
        Renders the html content and stores it in the db
    '''
    json_dict = {}
    event_details = {}
    tab_details = {}
    tab_details_list = []
    update_details = {}
    update_details_list = []

    # finding event_pk
    event_underscore_posn = event_json_filepath.find('_')
    event_pk = event_json_filepath[event_name_start_posn : event_underscore_posn]
    
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
    
    #event_spons_list : list containing spons for each event
    event_spons_list = list()
    for i in EVENT_SPONS:
        if i.keys()[0] == event_details['title']:
            event_spons_list = i[i.keys()[0]]
    
    context_dict = {'event' : event_details, 'tab_list': tab_details_list, 'updates_list': update_details_list, 'time_now':time_now, 'event_pk':event_pk, 'event_spons_list': event_spons_list}
    html_content = render_to_string('events/small/event_page.html', context_dict)
    
    if Event_html_dump.objects.filter(event_pk = event_pk).count() == 1:
        event_dump = Event_html_dump.objects.get(event_pk = event_pk)
        event_dump.html_content = html_content
        event_dump.save()
        return
    elif Event_html_dump.objects.filter(event_pk = event_pk).count() == 0:
        Event_html_dump.objects.create(event_pk = event_pk, html_content = html_content)
        return
    else:
        raise Exception
