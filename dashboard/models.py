from django.db import models
from events.models import *
from users.models import *
# Create your models here.

class TeamEvent(models.Model):
    team_id = models.CharField(default=0,null=True)
    team_name = models.CharField(max_length = 30,blank = True,null=True)
    users = models.ManyToManyField(User, blank = True, null = True)
    is_active = models.BooleanField(default = True)
    event       = models.ForeignKey(GenericEvent, related_name = 'userevents')
    #permissions = models.ManyToManyField(Permission, blank = True, null = True)
    def size(self):
        return len(self.users.all())
    def save(self, *args, **kwargs):
        #Here, for event title, TODO:shorthand version of the name needed, for now truncated
        self.team_id = 'TEAM#'+ str(event.title)[:5]+'#'+  +str(self.id)
        super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%(project_name)s - %(user_name)s" % { 'project_name' : str(self.event), 'user_name' : self.user.username }


#Updates for each user:: The user will get this on login:: He has to approve

UPDATE_CHOICES = (
    ('Team Add', 'Team Add'),
    ('Deadline for Registration', 'Deadline for Registration'),
    ('Deadline for Registration', 'Deadline for Registration'),
    )
class Update(models.Model):
    tag     = models.CharField(max_length = 20)
    content = models.CharField(max_length = 40)
    user    = models.ForeignKey(User, related_name = 'userupdates')
