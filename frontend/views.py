# Create your views here.
import django
import sha,random
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django.contrib import messages as MESGS

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User, Group
from django.template.context import Context, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, \
    logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.decorators import login_required
#from events.models import Event
from users.models import UserProfile, College
from django.utils.translation import ugettext as _
from users.forms import *
from django.contrib.sessions.models import Session
from misc.dajaxice.core import dajaxice_functions
from users.models import STATE_CHOICES

def home(request):  
    form=LoginForm()
    form_registration=AddUserForm()
    colllist=[coll.name+' | '+coll.city for coll in College.objects.all()]
    collstr=''
    for l in colllist:
        collstr+="\""+l+"\""+","
    collstr=collstr[:len(collstr)-1]
    stlist=[st[0] for st in STATE_CHOICES]
    return render_to_response ('home/home.html', locals(), context_instance=RequestContext(request))

#@login_required
def dashboard(request):
#    profile = UserProfile.objects.get(user=request.user)
    return render_to_response('dashboard/dashboard.html',locals(),context_instance=RequestContext(request))

def serenity(request):
    return render_to_response ('index.html', locals(), context_instance=RequestContext(request))
