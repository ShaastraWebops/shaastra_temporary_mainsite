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
from models import TeamEvent
from users.models import *
@dajaxice_register
def register_event(request,event_id,**kwargs):
    dajax=Dajax()
    i=0
    shalist=[]
    erp_db = DATABASES.keys()[1]
    event=ParticipantEvent.objects.using(erp_db).get(id=event_id)
    teamevent = TeamEvent.objects.create(event_id=event.id)
    teamevent.save()
    sha=''
    while 1>0:
        try:
            sha = kwargs['teammate#%d' % i]
            if sha!='':
                shalist.append(sha)
        except:
            break
        i=i+1
    #check for duplicates
    #TODO: find actual entries first(without '')
    if len(shalist) == 0:
        dajax.script('$.bootstrapGrowl("Please fill the form with shaastra id\'s of your teammates",{type:"danger"})')
        return dajax.json()

    if len(shalist)!=len(set(shalist)):
        dajax.script('$.bootstrapGrowl("No duplicate entries allowed in teammates",{type:"danger"})')
        return dajax.json()
    userlist=[]
    userlist.append(request.user)
    up=None
    for sha in shalist:
        try:
            up = UserProfile.objects.get(shaastra_id = sha)
            userlist.append(up.user)
        except:
            dajax.script('$.bootstrapGrowl("One/more of shaastra id\'s entered are invalid!",{type:"danger"})')
            return dajax.json()
    teamevent.users=userlist
    teamevent.is_active = True
    teamevent.save()
    dajax.script('$.bootstrapGrowl("Your team was registered successfully to event %s",{type:"success"})'% event.title)
    dajax.script('$.bootstrapGrowl("Your team ID: %s",{type:"success"})'% teamevent.team_id)
    dajax.script('$("#event_register").modal("toggle")')
    #TODO: create updates for other users
    return dajax.json()

@dajaxice_register
def register_event_form(request,event_id = None):
    dajax = Dajax()
    #: if user has chosen a college in dropdown, depopulate it OR growl
    if event_id is None:
        dajax.script('$.bootstrapGrowl("Invalid Event specified.", {type:"danger",timeout:50000} );')
        return dajax.json()
    else:
        try:
            erp_db = DATABASES.keys()[1]
            event = ParticipantEvent.objects.using(erp_db).get(id=event_id)
            if not request.user.is_authenticated():
                dajax.script('$.bootstrapGrowl("Please Login to register!", {timeout:50000} );')
                dajax.script('$("#login").show();')
                return dajax.json()
            user = request.user
        except:
            dajax.script('$.bootstrapGrowl("Invalid Event specified", {type:"danger",timeout:50000} );')
        if not event.registrable_online:
            dajax.script('$.bootstrapGrowl("You cannot register online for this event", {type:"danger",timeout:50000} );')
            return dajax.json()
        elif event.registration_starts and event.registration_ends:
            if event.registration_starts > timezone.now():
                days = (event.registration_starts - timezone.now()).days
                dajax.script('$.bootstrapGrowl("Please wait until %d days for registrations to open", {type:"danger",timeout:100000} );' % days)
                return dajax.json()
            elif event.registration_ends < timezone.now():
                dajax.script('$.bootstrapGrowl("Registrations closed! Sorry", {type:"danger",timeout:100000} );')
                return dajax.json()
            else:
                maxteam = event.team_size_max
                if maxteam >1:
                    dajax.script('$.bootstrapGrowl("Note that you need to have a team of atleast %d members to register", {timeout:50000} );'% event.team_size_max)
                    teammates = range(maxteam-1)
                    inputhtml = ""
                    for i in teammates:
                        inputhtml +="\'teammate#%d\':$(\'#shid_%d\').val()," %(i,i)
                    inputhtml=inputhtml[:len(inputhtml)-1]
                    context_dict = {'event': event,'teammates':teammates,'inputhtml':inputhtml,'team_max':maxteam-2}
                else:
                    #TODO : register him for the event
                    tev = TeamEvent(event_id=event.id)
                    tev.save()
                    tev.users.add(request.user)
                    tev.save()
                    dajax.script('$.bootstrapGrowl("You have been registered for the event: %s.", {timeout:50000} );'% event.title)
                    enddate = event.registration_ends
                    dajax.script('$.bootstrapGrowl("Deadline for the event is %s/%s/%s", {timeout:50000} );'% (enddate.day,enddate.month,enddate.year))
                    return dajax.json()
                html_stuff = render_to_string('dashboard/event_registration_form.html',context_dict,RequestContext(request))
                if html_stuff:
                    dajax.assign('#FormRegd','innerHTML',html_stuff)
                    dajax.script('$("#event_register").modal();')
        else:
            dajax.script('$.bootstrapGrowl("Registrations not put up yet, please wait!", {timeout:50000} );')
    return dajax.json()

