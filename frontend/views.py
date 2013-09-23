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
#from events.models import Event
from users.models import UserProfile, College
from django.utils.translation import ugettext as _
from users.forms import *
from django.contrib.sessions.models import Session
from misc.dajaxice.core import dajaxice_functions

def homee(request):
    return HttpResponse('ssup')

def logout(request):
    auth_logout(request)
    logged_in=True
    print 'logged out'
    print request.user.username
    #MESGS.success(request, msg_super)
    #form_registration=AddUserForm()
    #form=LoginForm()
    return HttpResponseRedirect('/')
    #return render_to_response ('home/home.html', locals(), context_instance=RequestContext(request))
    
def home(request):  
    form=LoginForm()
    if request.user.is_authenticated():
        logged_in=True
    form_registration=AddUserForm()
    return render_to_response ('home/home.html', locals(), context_instance=RequestContext(request))

def login(request):
    if request.user.is_authenticated():
        msg_login='%s, You are logged in!!' % request.user.username
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid() :
            data=form.cleaned_data
            username=data['username']
            password=data['password']
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                currentuser=user
                print currentuser.username
                logged_in=True
                msg='Hi %s' % request.user.username
                return HttpResponseRedirect('/')
            else:
                msg = 'Username and Password does not match!!!'  
                form = LoginForm()
                return render_to_response('home/home.html',locals(),context_instance=RequestContext(request))
    if request.method == 'GET':
        form = LoginForm()
        try:
            msg=request.session['msg']
            del request.session['msg']
        except:
            msg=''
        return render_to_response('home/home.html', locals(),
                                  context_instance=RequestContext(request))
    return HttpResponseRedirect('/')
   
def register(request):
    if request.method=="POST":
        form = AddUserForm(request.POST)
        print "comes"
        if form.is_valid():
            print "here"
            data = form.cleaned_data
            new_user = User(first_name=data['first_name'],last_name=data['last_name'], username=data['username'], email=data['email'])
            new_user.set_password(data['password']) 
            new_user.save()
            x = 1300000 + new_user.id 
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt + new_user.username).hexdigest()
            userprofile = UserProfile(user=new_user,activation_key=activation_key,gender=data['gender'],age=data['age'],branch=data['branch'],mobile_number=data['mobile_number'],college=data['college'],college_roll=data['college_roll'],shaastra_id= ("SHA" + str(x)),)
            print 'registered'
            userprofile.save()
            print "here"
            logged_in=True
            currentuser = authenticate(username=new_user.username, password=data['password'])
            if currentuser:
                print 'hi'
                auth_login(request,currentuser)
                #code for first time login
                return HttpResponseRedirect('/')
        else:
            print 'ERROROROROR'
            ifreg=True
            form_registration=form
            form=LoginForm()
#           logged_in=True
            msg_login='%s, You are logged in!!' % request.user.username
            return render_to_response('home/home.html', locals(),
                                  context_instance=RequestContext(request))
    if request.method == 'GET':
        form_registration = AddUserForm()
        try:
            msg=request.session['msg']
            del request.session['msg']
        except:
            msg=''
        return render_to_response('home/home.html', locals(),
                                  context_instance=RequestContext(request))
    form_registration=AddUserForm()
    return HttpResponseRedirect('/')

def serenity(request):
    return render_to_response ('index.html', locals(), context_instance=RequestContext(request))
