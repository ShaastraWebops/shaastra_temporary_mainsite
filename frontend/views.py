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
erp_db = settings.DATABASES.keys()[1]

eventlist = ['Aerobotics',
 'Lunar Rover Challenge',
 'Fire n Ice',
 'Contraptions',
 'Paper and Poster Presentation',
 'Forensics',
 'Vittaneeti',
 'Wright Design',
 'Hovercraft Workshop',
 'Online Puzzle Champ',
 'Shaastra Circuit Design Challenge',
 'Project X',
 'Robo Oceana',
 'Math Modelling',
 'How Things Work',
 'Paper Planes',
 'Chuckglider Workshop',
 'Quadrotor Workshop',
 'Case Study',
 'Robowars',
 'Chemical X',
 '3D Animation Workshop',
 'Desmod',
 'Shaastra Cube Open',
 'Shaastra Main Quiz',
 'Autonomous Robotics Workshop',
 'Master Builder',
 'Robotics',
 'Debugging',
 'Reverse Coding',
 'Junkyard Wars',
 'TopGun',
 'Streax Workshop',
 'Shaastra Junior Quiz',
 'Estimus',
 'Ultimate Engineer',
 'Online Math Modelling',
 'Code Obfuscation',
 'Forensics Workshop',
 'Open Programming Contest',
 'Hackfest Workshop',
 'Android Development Workshop',
 'Puzzle Champ',
 'Sustainable Cityscape',
 'Rubiks Cube Workshop',
 'Manual Robotics Workshop',
 'Onspot Desmod',
 'Auto Quiz',
 'Paper Plane Workshop',
 'Triathlon',
 'Finance and Consultancy',
 'Boeing National Aeromodelling Competition',
 'Automania',
 'Ideas Challenge',
 'Pan IIT Research Expo',
 'Ericsson Industry Defined Problem',
 'Eaton Industry Defined Problem',
 'GE Industry Defined Problem']


def home(request):  
    form=LoginForm()
    form_registration=AddUserForm()
    if request.method == 'POST':
        form_feedback = Feedback(request.POST)
        if form_feedback.is_valid():
            cd = form_feedback.cleaned_data
            form_feedback.save();
            if form_feedback.cleaned_data['any_other_suggestions']:
                feedback_message = "Thank You. We will make Shaastra 2015 a better Shaastra with your suggestions"
            #print cd['any_other_suggestions']
            else:
                feedback_message = "Thank You for your feedback."
            return render_to_response ('home/home.html', locals(), context_instance=RequestContext(request))
    else:
        form_feedback = Feedback()
    

    form_feedback=Feedback()
    #eventlist = [event.title for event in ParticipantEvent.objects.using(erp_db).all()]
    colllist=[coll.name+' | '+coll.city for coll in College.objects.all()]
    collstr=''
    eventstr=''
    for ev in eventlist:
        eventstr+="\"" + ev + "\"" +","
    eventstr=eventstr[:len(eventstr)-1]
    for l in colllist:
        collstr+="\""+l+"\""+","
    collstr=collstr[:len(collstr)-1]
    stlist=[st[0] for st in STATE_CHOICES]
#    try:
#        if request.session['file_upload']:
#            msg_file_upload = request.session['file_upload']
#            del request.session['file_upload']
#    except:
#        pass
    msg_file_upload = request.session.get('file_upload','')
    MEDIA_URL = settings.MEDIA_URL

    return render_to_response ('home/home.html', locals(), context_instance=RequestContext(request))

#@login_required
def dashboard(request):
#    profile = UserProfile.objects.get(user=request.user)
    try:
        if request.session['file_upload']:
            msg_file_upload = request.session['file_upload']
            del request.session['file_upload']
    except:
        pass
    SITE_URL = settings.SITE_URL
    #up_list = [up for up in UserProfile.objects.all()]
    return render_to_response('dashboard/dash_new.html',locals(),context_instance=RequestContext(request))

def serenity(request):
    return render_to_response ('index.html', locals(), context_instance=RequestContext(request))
