#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings
import os
#from events.models import Event
def upload_handler(model_name):
    def upload_func(instance, filename):
        return os.path.join(model_name, instance.title, filename)
    return upload_func


GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

STATE_CHOICES = (
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu And Kashmir', 'Jammu And Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Orissa', 'Orissa'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman And Nicobar Islands', 'Andaman And Nicobar Islands'),
    ('Chandigarh', 'Chandigarh'),
    ('Dadra And Nagar Haveli', 'Dadra And Nagar Haveli'),
    ('Daman And Diu', 'Daman And Diu'),
    ('Lakshadweep', 'Lakshadweep'),
    ('NCT/Delhi', 'NCT/Delhi'),
    ('Puducherry', 'Puducherry'),
    ('Outside India', 'Outside India'),
    )

class College(models.Model):

    name = models.CharField(max_length=255,
                            help_text='The name of your college. Please refrain from using short forms.'
                            )
    city = models.CharField(max_length=30,
                            help_text='The name of the city where your college is located. Please refrain from using short forms.'
                            )
    state = models.CharField(max_length=40, choices=STATE_CHOICES,
                             help_text='The state where your college is located. Select from the drop down list'
                             )

    def __unicode__(self):
        return '%s, %s, %s' % (self.name, self.city, self.state)

    class Admin:

        pass

class UserProfile(models.Model):

    user = models.ForeignKey(User, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
                              default='F')  # Defaults to 'girl' ;-)
    age = models.IntegerField(default=18)
                              # help_text='You need to be over 12 and under 80 years of age to participate'
                              # No age limit now.
    branch = models.CharField(max_length=50, blank=True, null=True,
                              help_text='Your branch of study')
    mobile_number = models.CharField(max_length=15, blank=True, null=True,
            help_text='Please enter your current mobile number')
    college = models.ForeignKey(College, null=True, blank=True)
    college_roll = models.CharField(max_length=40, null=True)

    shaastra_id = models.CharField(max_length = 20, unique = True, null=True)

    activation_key = models.CharField(max_length=40, null=True)
    #key_expires = models.DateTimeField(null=True)
    want_accomodation = models.BooleanField(default=False, help_text = "This doesn't guarantee accommodation during Shaastra.")
    is_core = models.BooleanField(default=False)
    is_hospi = models.BooleanField(default=False)

#    is_coord        = models.BooleanField....(default = False)

#    is_coord_of = models.ForeignKey(Event, null=True)

#    registered      = models.ManyToManyField(Event, null=True, related_name='registered_users')        #Events which this user has registered for

#    facebook_id = models.CharField(max_length=20)
#    access_token = models.CharField(max_length=250)
#    registered_events = models.ManyToManyField(Event,
#            related_name='participants', null=True)

    def __unicode__(self):
        return self.user.first_name

    class Admin:

        pass
import os
class shows_updates(models.Model):
    shows_name = models.CharField(max_length=255,
                            help_text='Name of the Show'
                            )
    update    = models.CharField(max_length=255,
					   help_text='Update field'
					        )
    def __unicode__(self):
        return '%s  %s'%(self.show_name,self.update)
    class meta:
        ordering=['-id']
        
EVENT_CATEGORIES = (
    ('Aerofest', 'Aerofest'),
    ('Coding', 'Coding'),
    ('Design and Build', 'Design and Build'),
    ('Involve', 'Involve'),
    ('Quizzes', 'Quizzes'),
    ('Online', 'Online'),
    ('Department Flagship', 'Department Flagship'),
    ('Spotlight', 'Spotlight'),
    ('Workshops', 'Workshops'),
    ('Exhibitions', 'Exhibitions and Shows'),
    ('Associated Events', 'Associated Events'),
    ('Sampark', 'Sampark'),
    )

UPDATE_CATEGORY = (
    ('Major Update', 'Major Update'),
    ('Updates', 'Updates'),
    )

class Tag(models.Model):
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
    events_logo = models.FileField(upload_to=upload_handler('eventslogo'),
        blank=True, null=True)
    spons_logo = models.ForeignKey(SponsLogoUploads, blank=True, null=True)
    
    def __unicode__(self):
        return self.title
    

class ParticipantEvent(GenericEvent):
    #event = models.ForeignKey(GenericEvent, unique=True)
    #Registration
    registrable_online = models.BooleanField(default=False,
            help_text='Can participants register online')
    begin_registration = models.BooleanField(default=False)
    registration_starts = models.DateTimeField(blank=True, null=True,
            help_text='Start Registration: YYYY-MM-DD hh:mm')
    registration_ends = models.DateTimeField(blank=True,null=True,
            help_text='End Registration: YYYY-MM-DD hh:mm')

    #Teams
    team_event = models.BooleanField(default=False,
            help_text='Is this a team event ?')
    team_size_min = models.IntegerField(default=1,
            help_text='Minimum team size')
    team_size_max = models.IntegerField(default=1,
            help_text='Maximum team size')

    #Submissions
    has_tdp = models.BooleanField(default=False,
            help_text='Does this event require participants to submit TDP ?')
    has_questionnaire = models.BooleanField(default=False,
            help_text='Does this event require participants to answer a questionnaire ?')
    
    #no need of __unicode__ as it is inherited from GenericEvent

class AudienceEvent(GenericEvent):
    #event = models.ForeignKey(GenericEvent, unique=True)
    video = models.URLField(blank=True, null=True, 
            help_text='URL of teaser')


'''class Tab(models.Model):
    
    Tabs for a particular event eg - Event Format, FAQ etc
    
    event = models.ForeignKey(GenericEvent,blank=True, null=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    pref = models.IntegerField(max_length=2, default=0, blank=False,
            help_text='The order in which your tabs will be displayed')

    def __unicode__(self):
        return self.title

    def delete(self):
        tabfiles = self.tabs.all()
        for tabfile in tabfiles:
            tabfile.delete()
        super(Tab,self).delete()

    class Meta:
        ordering = ['pref']

class TabFile(models.Model):
    
    All files related to a particular tab
    
    title = models.CharField(max_length=50)
    tab_file = models.FileField(upload_to=upload_handler('tabfiles'))
    tab = models.ForeignKey(Tab, related_name='tabs')
    url = models.URLField()

    def __unicode__(self):
        return self.url

    def delete(self):
        os.remove(self.tab_file.name)
        super(TabFile,self).delete()

class Update(models.Model):
    subject = models.CharField(max_length=300)
    description = models.TextField()
    date = models.DateField(default=datetime.now)
    category = models.CharField(max_length=25, choices=UPDATE_CATEGORY,
            help_text='You can add 4 Updates and 1 Announcement.\
            Mark as Announcement only if info is of utmost importance')
    event = models.ForeignKey(GenericEvent, blank=True, null=True)
    expired = models.BooleanField(default=False,
            help_text='Mark an update expired if it is no longer relevant\
            or if you have more than 4 Updates and 1 Announcement')

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
'''

class Sponsor(models.Model):
    name = models.CharField(max_length=20,
            help_text='Enter Company name')
    index_number = models.IntegerField(blank=True,
            help_text='Indicates order of importance - Most important is 1')

    def __unicode__(self):
        return self.name
