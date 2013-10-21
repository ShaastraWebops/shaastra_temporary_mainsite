# Create your views here.
import django
from django import forms
import sha,random
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.contrib import messages as MESGS
from django.core.exceptions import ObjectDoesNotExist
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
from django.utils import timezone
from dashboard.models import TDPFileForm,TeamEvent,Update
from django.core.exceptions import ValidationError

def submit_tdp(request):
    if not request.user.is_authenticated():
        #TODO: redirect him to mainsite , and pop the login modal
        return HttpResponse('Please login to submit TDP\'s')
    if not request.POST or not request.FILES:
        return HttpResponse('Incorrect URL.Click <a href="">here</a> to go back to mainsite.')
    fileform = TDPFileForm(request.POST,request.FILES)
    if not fileform.files:
        #TODO: submit tdp button comes only if upload succesful event of input type file
        return HttpResponse('Please upload a valid file')
    try:
        tdp = fileform.save(commit = False)
    except:
        request.session['file_upload'] = 'TDP Upload Failed: Illegal Characters in Filename'
        return HttpResponseRedirect(settings.SITE_URL+'#dashboard')
    tdp.teamevent = TeamEvent.objects.get(id = request.POST['teameventid'])
    
#        tdp.file_tdp.name
    try:
#    if 1:
        tdp.save()
        request.session['file_upload'] = 'TDP Upload Successful for %s!'% tdp.teamevent.get_event().title
        msg_success = 'Your TDP for %s was successfully submitted!' % tdp.teamevent.get_event().title
        update = Update(tag = 'TDP Submission',content = '',user = request.user)
        update.save()
    except ValidationError as e:
        errors=str(e)
        errors=errors[2:]
        errors=errors[:-2]
        request.session['file_upload'] = errors
        
    except:
        return HttpResponse('Unknown Error. Please contact WebOps Team.Go <a href = "%s">back</a> to mainsite'%settings.SITE_URL)
    return HttpResponseRedirect(settings.SITE_URL+'#dashboard')

def forgot_password(request,password_key = None):
    SITE_URL = settings.SITE_URL
    if request.user.is_authenticated():
        msg = "You are logged in!!"
    if request.method=='POST':
        reset_password_form = ResetPasswordForm(request.POST)
        success=True
        if reset_password_form.is_valid() and request.POST.has_key('user'):
            profile = UserProfile.objects.get(user__username=request.POST['user'])
            password = reset_password_form.cleaned_data['password']
            profile.user.set_password(password)
            profile.save()
            return HttpResponse('You have successfully changed your password!!!Visit our site here: <a href="%s">SHAASTRA</a>'% SITE_URL)
        else:
            return render_to_response('users/reset_password_form.html', locals(), context_instance = RequestContext(request))
    if (password_key == '' or password_key==None):
        msg="Key error, Please recheck the link sent to your registered email id"
    try:
        profile = UserProfile.objects.get(activation_key = str(password_key))
        user = profile.user
        x = 1300000 + profile.user.id 
        salt = sha.new(str(random.random())).hexdigest()[:5]
        profile.activation_key = sha.new(salt + user.username).hexdigest()
        profile.save()
        reset_password_form = ResetPasswordForm()
        success=True
    except:
        msg = 'Malicious url: Please check the link sent to your email id to reset your password'
    return render_to_response('users/reset_password_form.html', locals(), context_instance = RequestContext(request))


def activate(request, a_key = None ): 
    """
       The activation_key (a_key) is trapped from the url. If the key is not empty then the corresponding userprofile object is retrieved. If the object doesn't exist and ObjectDoesNotExist error is flagged.
       
       The the key has already expired then the userprofile and the corresponding user objects are deleted, otherwise, the is_active field in the user model is set to true.
       
       Note that, if is_active is not set to true, the user cannot login. 
    """
    SITE_URL = settings.SITE_URL
    link_to_site = False
    if (a_key == '' or a_key==None):
        msg="Key error"
    else:
        try:
            
            user_profile = UserProfile.objects.get(activation_key = a_key)
            if user_profile.user.is_active == True:
                msg="%s, Your account is already activated. Please visit our site at :"% user_profile.user.username
                link_to_site = True
            elif user_profile.key_expires < timezone.now():
                print 'EXPIRED'
                user = user_profile.user
                user.delete()
                user_profile.delete()
                msg="Sorry, your activation key expired, please register again"
            else:
                user = user_profile.user
                user.is_active = True
                user.save()
                user_profile.save()
                x = 1400000 + user_profile.user.id
                salt = sha.new(str(random.random())).hexdigest()[:5]
                user_profile.activation_key = sha.new(salt + user.username).hexdigest()
                user_profile.save()
        
                msg="Hi %s, You have been successfully registered. Please visit our site at:"% user_profile.user.username
                link_to_site = True
        except ObjectDoesNotExist:
            msg = "Incorrect activation key, please check the link you copied on your browser"
        # try-except-else is actually there! God knows what for... Nested try blocks work just as well...
        except :
            msg = "Activation Error, please contact our webOps Team"
            link_to_site  = True
    return render_to_response('users/activation_process.html',locals(), context_instance= RequestContext(request))


#def logout(request):
#    auth_logout(request)
#    logged_in=True
#    print 'logged out'
#    print request.user.username
#    #MESGS.success(request, msg_super)
#    #form_registration=AddUserForm()
#    #form=LoginForm()
#    return HttpResponseRedirect('/')
#    #return render_to_response ('home/home.html', locals(), context_instance=RequestContext(request))

#def login(request):
#    if request.user.is_authenticated():
#        msg_login='%s, You are logged in!!' % request.user.username
#    if request.method == 'POST':
#        form = LoginForm(request.POST)
#        if form.is_valid() :
#            data=form.cleaned_data
#            username=data['username']
#            password=data['password']
#            user = authenticate(username=username, password=password)
#            if user:
#                #to implement: is_active!!!!!!!!!!
#                if not user.is_active:
#                    msg = 'Please click the activation link sent to your registered email id'
#                    return HttpResponseRedirect('/')
#                auth_login(request, user)
#                currentuser=user
#                print currentuser.username
#                logged_in=True
#                msg='Hi %s' % request.user.username
#                return HttpResponseRedirect('/')
#            else:
#                msg = 'Username and Password does not match!!!'  
#                form = LoginForm()
#                form_registration = AddUserForm()
#                return render_to_response('home/home.html',locals(),context_instance=RequestContext(request))
#    if request.method == 'GET':
#        form = LoginForm()
#        form_registration = AddUserForm()
#        try:
#            msg=request.session['msg']
#            del request.session['msg']
#        except:
#            msg=''
#        return render_to_response('home/home.html', locals(),
#                                  context_instance=RequestContext(request))
#    return HttpResponseRedirect('/')

