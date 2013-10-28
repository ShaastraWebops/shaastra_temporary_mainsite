from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings
from django.utils import timezone
# from erp
from mainsite_2014.settings import MEDIA_ROOT
#from shaastra_mainsite_2014_temp.variables import events_being_edited
# From form
#from events.forms import get_json_file_path, EditError
# python imports
import json
import os

# Create your models here.
EVENT_CATEGORIES = (
    ('Aerofest', 'Aerofest'),
    ('Coding', 'Coding'),
    ('Design and build', 'Design and build'),
    ('Involve', 'Involve'),
    ('Quizzes', 'Quizzes'),
    ('Online', 'Online'),
    ('Department Flagship Event', 'Department Flagship Event'),
    ('Spotlight', 'Spotlight'),
    ('Workshops', 'Workshops'),
    ('Exhibitions', 'Exhibitions and Shows'),
    ('Miscellaneous', 'Miscellaneous'),
    ('Sampark', 'Sampark'),
    ('B- Events','B- Events'),
    )

UPDATE_CATEGORY = (
    ('Major Update', 'Major Update'),
    ('Updates', 'Updates'),
    )
    
EVENT_TYPE = (
    ('Audience', 'Audience'),
    ('Participant', 'Participant'),
    ('None','None'),
    )

#Checks if the directory exists and creates it if not
def upload_handler(name):
    if not os.path.exists('%s/events/' % (MEDIA_ROOT)+name):
        os.makedirs('%s/events/' % (MEDIA_ROOT)+name)
    return '%s/events/' % (MEDIA_ROOT)+name
 
class Tag(models.Model):
    '''
    For searching
    '''
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name

class SponsLogoUploads(models.Model):
    logo1 = models.FileField(upload_to=upload_handler('sponslogo'), blank=True, null=True)
    logo2 = models.FileField(upload_to=upload_handler('sponslogo'), blank=True, null=True)
    logo3 = models.FileField(upload_to=upload_handler('sponslogo'), blank=True, null=True)
    #more fields to be added when max number of uploads is known

class GenericEvent(models.Model):
    '''
    Events are of two types - Participant Events and Audience Events
    GenericEvents contains the common fields
    '''

    title = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    category = models.CharField(max_length=100, choices=EVENT_CATEGORIES)
    event_type = models.CharField(max_length=100, choices=EVENT_TYPE, blank=True, null=True,
            help_text='Select Participant only if your event is registrable, otherwise select Audience')
    events_logo = models.FileField(upload_to=upload_handler('eventslogo'),
        blank=True, null=True)
    spons_logo = models.ForeignKey(SponsLogoUploads, blank=True, null=True)
        
    
    def __unicode__(self):
        return self.title
    

class ParticipantEvent(GenericEvent):
    '''
    Registrable events - which need fields like when registration starts, team size etc
    '''
    #event = models.ForeignKey(GenericEvent, unique=True)
    #Registration
    registrable_online = models.BooleanField(default=False,
            help_text='Can participants register online')
    #begin_registration = models.BooleanField(default=False) # Varshaa : Based on below 2 fields, this can be got. DONE 
    registration_starts = models.DateTimeField(blank=True, null=True,
            help_text='Start Registration: YYYY-MM-DD hh:mm')
    registration_ends = models.DateTimeField(blank=True,null=True,
            help_text='End Registration: YYYY-MM-DD hh:mm')

    #Teams
    #team_event = models.BooleanField(default=False, # Varshaa : Based on below 2 fields, this can be got. DONE
            #help_text='Is this a team event ?')
    team_size_min = models.IntegerField(default=1,
            help_text='Minimum team size',blank=True,null=True)
    team_size_max = models.IntegerField(default=1,
            help_text='Maximum team size',blank=True,null=True)

    #Submissions -- This year, even questionnaire is called a tdp. DONE
    has_tdp = models.BooleanField(default=False, 
            help_text='Does this event require participants to submit TDP ?')
    
    def days_left(self):
        return (self.registration_ends - timezone.now()).days
    
    def hours_left(self):
        return (int)((self.registration_ends - timezone.now()).seconds/3600)
    #no need of __unicode__ as it is inherited from GenericEvent

class AudienceEvent(GenericEvent):
    '''
    For such events we don't need registration - like Shows etc 
    '''
    #event = models.ForeignKey(GenericEvent, unique=True)
    video = models.URLField(blank=True, null=True, 
            help_text='URL of teaser')


class Tab(models.Model):
    '''
    Tabs related to an event eg - Event Format, FAQ etc
    '''
    event = models.ForeignKey(GenericEvent,blank=True, null=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    pref = models.IntegerField(max_length=2, default=0, blank=False,
            help_text='The order in which your tabs will be displayed')

    def __unicode__(self):
        return self.title

#    def delete(self): #For deleting a tab, we need to delete all tabfiles also 
#        '''
#            -> delete all tabfiles related to the tab
#            -> delete the keys from the JSON file that belong to this tab
#            -> check if the event JSON file is already being edited
#        '''
#        tabfiles = self.tabs.all() #'tabs' is the name that relates(backward) Tabs to Tabfiles
#        for tabfile in tabfiles:
#            tabfile.delete()
#        
#        # importing the below stuff at the top of this file gives import error. need to find a fix for this.
#        from events.forms import get_json_file_path, EditError
#        tab_pk = self.pk
#        event_inst = self.event
#        event_pk = event_inst.pk
#        event_title = event_inst.title
#        file_path = get_json_file_path(str(event_pk)+'_'+event_title+'.json')
#        
#        if os.path.exists(file_path):
#            with open(file_path) as f:
#                json_data = json.load(f)
#                for key in json_data.keys():
#                    if key.startswith('tab'+str(tab_pk)+'_'):
#                        json_data.pop(key)
#                f.close()
#            
#            if event_pk in events_being_edited:
#                raise EditError('This event is being edited by some other user. Please try again later.')
#            
#            events_being_edited.append(event_pk)
#            with open(file_path, 'w') as f:
#                json.dump(json_data, f)
#                f.close()
#                events_being_edited.remove(event_pk)
#        else:
#            raise EditError('There is some error with this tab. Contact the WebOps Team')
#        
#        super(Tab,self).delete()

    class Meta:
        ordering = ['pref']

class TabFile(models.Model):
    '''
    All files related to a particular tab
    '''
    title = models.CharField(max_length=50)
    tab_file = models.FileField(upload_to=upload_handler('tabfiles'))
    tab = models.ForeignKey(Tab, related_name='tabs')
    url = models.URLField()

    def __unicode__(self):
        return self.url

#    def delete(self):
#        os.remove(self.tab_file.name)
#        super(TabFile,self).delete()

class Update(models.Model):
    '''
    Updates - related to an event 
    '''
    subject = models.CharField(max_length=300)
    description = models.TextField()
    date = models.DateField(default=datetime.now)
    category = models.CharField(max_length=25, choices=UPDATE_CATEGORY,
            help_text='You can add 4 Updates and 1 Major Update.\
            Mark as Major only if info is of utmost importance')
    event = models.ForeignKey(GenericEvent, related_name ='updates', blank=True, null=True)  # Varshaa : Give key from event to update (for easy querying)
    #Querying updates of an event can be done like this - EventObjectName.updates.all() 
    expired = models.BooleanField(default=False,
            help_text='Mark an update expired if it is no longer relevant\
            or if you have more than 4 Updates and 1 Major Update')

    def __unicode__(self):
        return self.subject

class Question(models.Model):
    q_number = models.IntegerField(max_length=2)
    title = models.TextField(max_length=1500, blank=False)
    
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['q_number']

class SubjectiveQuestion(Question):
    #question = models.ForeignKey(Question)
    event = models.ForeignKey(ParticipantEvent)

class ObjectiveQuestion(Question):
    #question = models.ForeignKey(Question)
    event = models.ForeignKey(ParticipantEvent)

class MCQOption(models.Model):
    question = models.ForeignKey(ObjectiveQuestion, null=True, blank=True)
    option = models.CharField(max_length=1)
    text = models.TextField(max_length=1000)

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['option']


class Sponsor(models.Model):
    '''
    Details about Sponsorers
    '''
    name = models.CharField(max_length=20,
            help_text='Enter Company name')
    index_number = models.IntegerField(blank=True,
            help_text='Indicates order of importance - Most important is 1')

    def __unicode__(self):
        return self.name
