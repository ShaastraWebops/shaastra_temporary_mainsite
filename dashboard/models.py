from django import forms
from django.db import models
from events.models import *
#from users.models import UserProfile
from mainsite_2014.settings import DATABASES
erp_db = DATABASES.keys()[1]
from time import gmtime,strftime
from django.utils import timezone
import datetime,sha,random
#Also set is_active to True each time created
class TeamEvent(models.Model):
    team_id     = models.CharField(default='0',null=True,max_length = 50)
    team_name   = models.CharField(max_length = 30,blank = True,null=True)
    users       = models.ManyToManyField(User, blank = True, null = True)
    is_active   = models.BooleanField(default = False)
    #permissions = models.ManyToManyField(Permission, blank = True, null = True)
    #TODO: add time of adding??
    event_id       = models.IntegerField(default=-1)#This will store id of participant event
    def size(self):
        return len(self.users.all())
        
    def save(self, *args, **kwargs):
        #Here, for event title, TODO:shorthand version of the name needed, for now truncated
        if self.event_id!=-1 and self.is_active == True:
            try:
               event=ParticipantEvent.objects.using(erp_db).get(id=self.event_id)
               self.team_id = 'TEAM#'+ str(event.title[:5])+'#'+str(self.pk)
            except:
                self.team_id = 'TEAM#'+ '#'+str(self.pk)
        super(TeamEvent, self).save(*args, **kwargs)
    def get_event(self):
        try:
            event =  ParticipantEvent.objects.using(erp_db).get(id = self.event_id)    
            return event
        except:
            return None
    def get_team(self):
        uplist = []
        for user in list(self.users.all()):
            up = user.get_profile()
            uplist.append(up)
        return uplist
    def clean(self):
        super(TeamEvent,self).clean()
        try:
            if self.users.count() > ParticipantEvent.objects.using(erp_db).get(id=self.event_id).team_size_max:
                self.is_active = False
            if len(self.users.all())!=len(set(self.users.all())):
                # duplicate users
                self.is_active = False
        except:
            pass
    def __unicode__(self):
        team_str = self.team_id
        if not team_str:
            team_str = "Not provided during registration"
        try:
            event=ParticipantEvent.objects.using(erp_db).get(id=self.event_id)
            return "Team id:%s, Team name: %s, Event:%s" % (self.team_id,team_str,event.title)
        except:
            return "Team id:%s, Team name: %s" % (self.team_id,self.team_name)
    #returns list of tdp's under team
    def get_tdp(self):
        return list(TDP.objects.filter(teamevent = self))
        
    # returns if tdp was submitted
    def has_submitted_tdp(self):
        if len(self.get_tdp()) > 0:
            return True
        return False

#function returns True is user is not in any team given the event id
def has_team(user,event_id = None):
    if event_id is None:
        return 'Need parameter: event id in erpDB','Need parameter: event id in erpDB'
    try:
        event = ParticipantEvent.objects.using(erp_db).get(id = event_id)
        teamEventList = TeamEvent.objects.filter(event_id = event.id)
        for teamevent in teamEventList:
            if user in teamevent.users.all():
                return 'has_team',teamevent.team_name
        return 'no_team','no_team'
    except:
        return 'give proper event id','give proper event id'

#Updates for each user:: The user will get this on login:: He has to approve

UPDATE_CHOICES = (
    ('Team Add', 'Team Add'),
    ('Deadline for Registration', 'Deadline for Registration'),
)

class Update(models.Model):
    tag     = models.CharField(max_length = 20)
    content = models.CharField(max_length = 200)
    user    = models.ForeignKey(User, related_name = 'userupdates')
#    time_added = models.DateTimeField(auto_now = True)
    #link    = models.?? on click user goes to where the update relates to


#ALLOWED_FILETYPE = ['doc','pdf','odt','txt','docx']
ALLOWED_FILETYPE = ['pdf']
def tdp_upload_handler(self,filename):
#    time =  strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()).replace(" ",'_')
    time = str(timezone.now().date())
    fname = str(filename).split('.')[-1]
    if (fname.split('.')[-1] not in ALLOWED_FILETYPE):
        raise forms.ValidationError("TDP Upload Failed, Use Please only Allowed File Types.")
    if self.file_tdp.size > 5300000:
        raise forms.ValidationError("Maximum File Upload Size is 5MB Exceeded. Given Size: %s MB"% str(self.file_tdp.size*1.0/(1024*1024))[:4])
    #randstr: 5 letter random string to prevent hacking of other team submissions
    randstr = sha.new(str(random.random())).hexdigest()[:5]
    url = 'tdpsubmissions/%s/%s_%s_%s_.%s'%(self.teamevent.get_event().title,self.teamevent.team_id,time,randstr,fname.split('.')[-1])
    #TODO: replace # by something else for url
    url = url.replace('#','_')
    return url


class TDP(models.Model):
    teamevent   = models.ForeignKey(TeamEvent,null = True,blank = True)
    file_tdp    = models.FileField(max_length = 100,upload_to =tdp_upload_handler,blank=True,null=True)
    def save(self,*args,**kwargs):
        if self.teamevent:
            #Check: if registration is not closed:
            if timezone.now()> self.teamevent.get_event().registration_ends:
                return 0
            if self.teamevent.tdp_set.all().count == 0:
                super(TDP,self).save(*args,**kwargs)
            else:
                tdplist = self.teamevent.tdp_set.all()
                #TODO: if invalid type, do NOT delete others, take lite
                super(TDP,self).save(*args,**kwargs)
                #Now, tdplist also contains self, so delete all tdp except existing one
                for tdp in tdplist:
                    if not self == tdp:
                        tdp.delete()
        else:
            super(TDP,self).save(*args,**kwargs)

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.file_tdp.storage, self.file_tdp.path
        # Delete the model before the file
        super(TDP, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
        
    def get_event(self):
        if event_id==-1:
            return None
        event = teamevent.get_event()
        return event

    def get_tdp_file(self):
        if self.file_tdp:
            return self.file_tdp
        return None
    
def get_tdp_event(event = None):
    if event is None:
        return None
    if not isinstance(event,ParticipantEvent):
        return None
    tdplist=[]
    for tdp in TDP.objects.using(settings.DATABASES.keys()[0]).all():
        if tdp.get_event() == event:
            tdplist.append((tdp,tdp.teamevent.team_id))
    if len(tdplist) == 0:
        return None
    return tdplist

class TDPFileForm(forms.ModelForm):
    class Meta:
        model = TDP
        exclude = ('teamevent',)
#    def __init__(self, *args, **kwargs):
#        from django.forms.widgets import HiddenInput
#        super(TDPFileForm, self).__init__(*args, **kwargs)
#        self.fields['teamevent'].widget = HiddenInput()

