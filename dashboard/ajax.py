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

@dajaxice_register
def register_event(request,**kwargs):
    dajax=Dajax()
    dajax.script('alert("success");')
    return dajax.json()

@dajaxice_register
def register_event_form(request,event_id = None):
    dajax = Dajax()
    print '********'
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
        if event.registration_starts and event.registration_starts:
            if event.registration_starts > timezone.now():
                days = (event.registration_starts - timezone.now()).days
                dajax.script('$.bootstrapGrowl("Please wait until %d days for registrations to open", {type:"danger",timeout:100000} );' % days)
                return dajax.json()
            if event.registration_ends < timezone.now():
                dajax.script('$.bootstrapGrowl("Registrations closed! Sorry", {type:"danger",timeout:100000} );' % days)
                return dajax.json()
        else:
            maxteam = event.team_size_max
            if maxteam >1:
                dajax.script('$.bootstrapGrowl("Note that you need to have a team of %d members to register", {timeout:50000} );'% event.team_size_max)
                teammates = range(maxteam-1)
                inputhtml = ""
                for i in teammates:
                    inputhtml +="\'teammate#%d\':$(\'#shid_%d\').val()," %(i,i)
                inputhtml=inputhtml[:len(inputhtml)-1]
                print '/////////////////'
                print inputhtml
                print '++++++++++++++++'
                context_dict = {'event': event,'teammates':teammates,'inputhtml':inputhtml}
            else:
                #TODO : register him for the event
                tev = TeamEvent(event=event)
                tev.save()
                tev.add(user)
                tev.save()
                dajax.script('$.bootstrapGrowl("You have been registerd for the event: %s.", {timeout:50000} );'% event.title)
                enddate = event.registration_ends
                dajax.script('$.bootstrapGrowl("Deadline for the event is %s/%s/%s", {timeout:50000} );'% (enddate.day,enddate.month,enddate.year))
                return dajax.json()
            html_stuff = render_to_string('dashboard/event_registration_form.html',context_dict,RequestContext(request))
            if html_stuff:
                dajax.assign('#FormRegd','innerHTML',html_stuff)
                dajax.script('$("#event_register").modal();')
    return dajax.json()

