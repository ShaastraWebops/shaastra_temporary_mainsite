import django
import sha,random
from django.utils import simplejson,timezone
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
from django.dispatch import receiver
from django.conf import settings
from models import *
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.template.loader import render_to_string
from django.template.context import Context, RequestContext
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from mainsite_2014.settings import DATABASES

from misc.dajaxice.utils import deserialize_form
from django.contrib.auth import authenticate

from django.core.mail import send_mail
from django.contrib import messages as MESGS
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.template.loader import get_template
from django.shortcuts import render_to_response, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.decorators import login_required
#from events.models import Event
from django.utils.translation import ugettext as _
from django.contrib.sessions.models import Session
from misc.dajaxice.core import dajaxice_functions

from django.utils import simplejson
from misc.dajaxice.decorators import dajaxice_register
from django.dispatch import receiver
import datetime
from models import TeamEvent,Update,has_team
from users.models import *

@dajaxice_register
def register_event(request,event_id=None,team_name=None,**kwargs):
    dajax=Dajax()
    if event_id is None or team_name is None:
        dajax.script('$.bootstrapGrowl("Invalid entry",{type:"danger",delay:10000})')
        return dajax.json()
    i=1
    shalist=[]
    erp_db = DATABASES.keys()[1]
    try:
        event=ParticipantEvent.objects.using(erp_db).get(id=event_id)
        if not event.registrable_online:
            dajax.script('$.bootstrapGrowl("Invalid event: can\'t register online!",{type:"danger",delay:10000})')
            #TODO: close the modal!!
            return dajax.json()
    except:
        dajax.script('$.bootstrapGrowl("Invalid event",{type:"danger",delay:10000})')    
        return dajax.json()
    teamevent = TeamEvent(event_id=event.id)
    profile = UserProfile.objects.get(user=request.user)
    sha=''
    while 1>0:
        try:
            sha = kwargs['teammate#%d' % i]
            if sha!='':
                if sha==profile.shaastra_id:
                    dajax.script('$.bootstrapGrowl("Enter your teammates\' ID\'s only. You will be registered automatically. You do no need to enter your ID",{type:"danger",delay:10000})')
                    return dajax.json()
                shalist.append(sha)
        except:
            break
        i=i+1
    #check for duplicates
    #TODO: find actual entries first(without '')
    if len(shalist)!=len(set(shalist)):
        dajax.script('$.bootstrapGrowl("No duplicate entries allowed.",{type:"danger",delay:10000})')
        return dajax.json()
    if len(shalist) < event.team_size_min-1:
        dajax.script('$.bootstrapGrowl("Minimum team size:%d!",{type:"danger",delay:10000})'% event.team_size_min)
        return dajax.json()
    
    userlist=[]
    userlist.append(request.user)
    up=None
    for sha in shalist:
        try:
            up = UserProfile.objects.get(shaastra_id = sha)
            msg,teamname = has_team(up.user,event.id)
            if msg =='has_team':
                dajax.script('$.bootstrapGrowl("One of your teammates: with id %s is already in another team named %s for this event.");$.bootstrapGrowl("A user can be part of only 1 team for an event",{type:"danger",delay:20000});'% (up.shaastra_id,teamname))
                return dajax.json()
            userlist.append(up.user)
        except:
            dajax.script('$.bootstrapGrowl("One/more of shaastra id\'s entered are invalid!",{type:"danger",delay:20000})')
            return dajax.json()
    teamevent.save()
    teamevent.users=userlist
    teamevent.is_active = True
    teamevent.team_name = team_name
    teamevent.save()
    try:
        for user in userlist:
            update = Update(tag='Event registration',content='Added to team: %s in event %s'%(teamevent.team_name,teamevent.get_event().title),user=user)
            update.save()
    #TODO: updates should not cause error
    except:
        pass
    dajax.script('$.bootstrapGrowl("Your team was registered successfully to event %s",{type:"success",delay:30000})'% event.title)
    dajax.script('$.bootstrapGrowl("Your team ID: %s",{type:"success",delay:100000})'% teamevent.team_id)
    dajax.script('$("#event_register").modal("toggle")')
    enddate = teamevent.get_event().registration_ends
    dajax.script('$.bootstrapGrowl("Note:Deadline for the event is %s/%s/%s", {delay:100000} );'% (enddate.day,enddate.month,enddate.year))
    #TODO: create updates for other users and him
    return dajax.json()

@dajaxice_register
def register_event_form(request,event_id = None):
    dajax = Dajax()
    #dajax.script("$('#gif_eventregister').hide()")
    #: if user has chosen a college in dropdown, depopulate it OR growl
    if event_id is None:
        dajax.script('$.bootstrapGrowl("Invalid Event specified.", {type:"danger",delay:10000} );')
        return dajax.json()
    else:
        try:
            erp_db = DATABASES.keys()[1]
            event = ParticipantEvent.objects.using(erp_db).get(id=event_id)
            if not request.user.is_authenticated():
                dajax.script('$.bootstrapGrowl("Please Login to register!", {delay:10000} );')
                dajax.script('$("#login").modal();')
                return dajax.json()
            user = request.user
        except:
            dajax.script('$.bootstrapGrowl("Invalid Event specified", {type:"danger",delay:20000} );')
            return dajax.json()
        if not event.registrable_online:
            dajax.script('$.bootstrapGrowl("You cannot register online for the event:%s", {type:"danger",delay:50000} );'% event.title)
            return dajax.json()
        elif event.registration_starts and event.registration_ends:
            if event.registration_starts > timezone.now():
                days = (event.registration_starts - timezone.now()).days
                dajax.script('$.bootstrapGrowl("Please wait until %d days for registrations to open for %s", {type:"danger",delay:10000} );' % (days,event.title))
                return dajax.json()
            elif event.registration_ends < timezone.now():
                dajax.script('$.bootstrapGrowl("Registrations closed for %s! Sorry", {type:"danger",delay:20000} );'% event.title)
                return dajax.json()
            else:
                maxteam = event.team_size_max
                minteam = event.team_size_min
#                maxteam=3
#                minteam=3
                if maxteam >1:
                    msg,team_name = has_team(request.user,event.id)
                    if msg =='has_team':
                        dajax.script('$.bootstrapGrowl("You are already a part of team:%s for this event. Multiple entries for same user is not allowed sorry", {delay:10000})'% str(team_name))
                        #TODO: close the 
                        return dajax.json()
                    if event.team_size_min>1:
                        dajax.script('$.bootstrapGrowl("Note that you need to have a team with atleast %d more members to register", {delay:100000} );'% (event.team_size_min-1))
                    else:
                        dajax.script('$.bootstrapGrowl("You can register alone, or with a maximum of %d teammates", {delay:100000} );'% (event.team_size_max-1))
                    teammates = range(minteam,maxteam)
                    teammates = teammates[:-1]
                    teammates_min = range(minteam)
                    inputhtml = ""
                    for i in (teammates_min+teammates)[:len(teammates_min+teammates)]:
                        inputhtml +="\'teammate#%d\':$(\'#shid_%d\').val()," %(i+1,i+1)
                    
                    inputhtml=inputhtml[:len(inputhtml)-1]
                    
                else:
                    msg,team_name = has_team(request.user,event.id)
                    if msg =='has_team':
                        dajax.script('$.bootstrapGrowl("You are already a part of team:%s for this event. Multiple entries for same user is not allowed sorry", {delay:20000});'%team_name);
                        return dajax.json()
                    #tev = TeamEvent(event_id = event.id)
                    #tev.save()
                    #tev.users.add(request.user)
                    #tev.save()
                    #update = Update(tag='Event registration',content='Added to team: %s in event %s'%(tev.team_name,tev.get_event().title),user=request.user)
                    #update.save()
                    #dajax.script('$.bootstrapGrowl("You have been registered for %s", {timeout:100000});' %event.title );
                    #TODO: update
                    inputhtml=''
                    teammates=[]
                    teammates_min=[]
                    #dajax.script('$("#event_register").modal("toggle");')
                    #return dajax.json()
                context_dict = {'event': event,'teammates':teammates,'teammates_min':teammates_min,'inputhtml':inputhtml,'team_max':len(teammates_min+teammates)-1,'minteam':minteam}
                html_stuff = render_to_string('dashboard/event_registration_form.html',context_dict,RequestContext(request))
                if html_stuff:
                    dajax.assign('#FormRegd','innerHTML',html_stuff)
                    dajax.script('$("#event_register").modal();')
        else:
            dajax.script('$.bootstrapGrowl("Registrations not put up yet, please wait!", {delay:10000} );')
    return dajax.json()

