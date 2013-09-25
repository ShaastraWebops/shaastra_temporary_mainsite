# For simple dajax(ice) functionalities
from django.utils import simplejson
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax

# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string

# Decorators
from django.contrib.auth.decorators import login_required, user_passes_test

# From Misc to show bootstrap alert
#from misc.utilities import show_alert

# From shaasta_mainsite_2014
from mainsite_2014.settings import DATABASES, ERP_PROJECT_PATH

#from events
from events.models import GenericEvent, EVENT_CATEGORIES

# Python imports
import json
import os


def get_category_json_file_path(filename):
    file_path = os.path.abspath( os.path.join( ERP_PROJECT_PATH, 'media','json') )
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return os.path.join(file_path, filename)

@dajaxice_register
def say_hello(request): 
    """
        Used for testing Dajax + Dajaxice
    """
    dajax = Dajax()
    dajax.alert("Hello World!")
    return dajax.json()

@dajaxice_register
def show_events_list(request):
    '''
        This function returns a json file containing events corresponding to each category.
        If this json file does not exist, it creates one.
        
        vars-
            event_category_dict: holds events corresponding to each category
            For generating json file:
                erp_db: holds the database alias of the erp database
                event_details_dict: holds pk, title, event_type of a particular event
                event_details_list: holds event_details_dict for all events in a particular category
            Data retrived from json file:
                event_list: holds events corresponding to the category requested
                Structure of event_list:
                    event_list = [ event1_details, event2_details, ... ]
                    event1_details, event2_details, etc. are events that belong to the requested category
                    These event_details are dicts of the format {'pk': event_pk, 'title': event_title, 'event_type':event_type}
    '''
    dajax = Dajax()
    event_category_dict = {}
    event_list = []
    
    event_category_filepath = get_category_json_file_path('event_category.json')
    if not os.path.exists(event_category_filepath):
        erp_db = DATABASES.keys()[1] # the key in DATABASES dict in settings.py corresponding to erp db
        for category in EVENT_CATEGORIES:
            event_queryset = GenericEvent.objects.using(erp_db).filter(category=category[0])
            
            event_details_list = []
            for event in event_queryset:
                event_details_dict = {}
                event_details_dict['pk'] = event.pk
                event_details_dict['title'] = event.title
                event_details_dict['event_type'] = event.event_type
                event_details_list.append(event_details_dict)
            
            event_category_dict[category[0]] = event_details_list
        with open(event_category_filepath, 'w') as f:
            json.dump(event_category_dict, f)
            f.close()
    else:
        with open(event_category_filepath) as f:
            event_category_dict = json.load(f)
            f.close()
    
    #render the content
    return simplejson.dumps(event_category_dict)

"""@dajaxice_register
def show_events_list(request, event_category=None, el_object_id=None):
    '''
        Shows the events corresponding to a particular category in FullscreenLayoutPageTransitions format.
        (Refer: http://tympanus.net/Development/FullscreenLayoutPageTransitions/)
        
        This function renders events from a json file containing events corresponding to each category.
        If this json file does not exist, it creates one.
        
        args-
            event_category: holds the event category received from the request
            el_object_id: id of the anchor tag of event_category
        vars-
            event_category_dict: holds events corresponding to each category
            For generating json file:
                erp_db: holds the database alias of the erp database
                event_details_dict: holds pk, title, event_type of a particular event
                event_details_list: holds event_details_dict for all events in a particular category
            Data retrived from json file:
                event_list: holds events corresponding to the category requested
                Structure of event_list:
                    event_list = [ event1_details, event2_details, ... ]
                    event1_details, event2_details, etc. are events that belong to the requested category
                    These event_details are dicts of the format {'pk': event_pk, 'title': event_title, 'event_type':event_type}
    '''
    dajax = Dajax()
    event_category_dict = {}
    event_list = []
    
    if not (event_category or el_object_id):
        show_alert(dajax, "error", "There is some error on the site, please report to WebOps team")
        return dajax.json()

    event_category_filepath = get_category_json_file_path('event_category.json')
    if not os.path.exists(event_category_filepath):
        erp_db = DATABASES.keys()[1] # the key in DATABASES dict in settings.py corresponding to erp db
        for category in EVENT_CATEGORIES:
            event_queryset = GenericEvent.objects.using(erp_db).filter(category=category[0])
            
            event_details_list = []
            for event in event_queryset:
                event_details_dict = {}
                event_details_dict['pk'] = event.pk
                event_details_dict['title'] = event.title
                event_details_dict['event_type'] = event.event_type
                event_details_list.append(event_details_dict)
            
            event_category_dict[category[0]] = event_details_list
        with open(event_category_filepath, 'w') as f:
            json.dump(event_category_dict, f)
            f.close()
    else:
        with open(event_category_filepath) as f:
            event_category_dict = json.load(f)
            f.close()
    
    try:
        event_list = event_category_dict[event_category]
    except:
        show_alert(dajax, "error", "There is some error on the site, please report to WebOps team")
        return dajax.json()
    
    #render the content
    context_dict = {'event_list' : event_list } #, 'category_name': event_category.lower()}
    html_content = render_to_string('events/small/events_list.html', context_dict, RequestContext(request))
    dajax.assign(".main_event_item", "innerHTML", html_content)
    dajax.script("$el_object = $( document.getElementById('"+el_object_id+"') );\
                  show_event_group($el_object);")
    
    return dajax.json()"""
