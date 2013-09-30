import django
import sha,random
from forms import AddUserForm,LoginForm
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
from forms import AddUserForm,LoginForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from misc.dajaxice.utils import deserialize_form
from django.contrib.auth import authenticate

from django.core.mail import send_mail
from django.contrib import messages as MESGS
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.template.context import Context, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
#from events.models import Event
from django.utils.translation import ugettext as _
from django.contrib.sessions.models import Session
from misc.dajaxice.core import dajaxice_functions

from models import *
from django.utils import simplejson
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
from django.dispatch import receiver
from django.template.loader import render_to_string
import datetime


@dajaxice_register
def add_college(request,college=None,city=None,state=None):
    dajax = Dajax()
    #TODO: get the Login modal back up
    
    #: if user has chosen a college in dropdown, depopulate it OR growl
    if city is None or college is None or state is None or city =='' or college =='' or state =='':
        dajax.script('$.bootstrapGrowl("Please enter relevant details for adding your college", {type:"danger",timeout:12000} );' )
        return dajax.json()
    else:
        try:
            for coll in College.objects.all():
                if coll.name.lower() == college.lower():
                    dajax.script('$.bootstrapGrowl("Your college is already on our list, please check again", {type:"danger",timeout:12000} );')
                    return dajax.json()    
#            coll=College.objects.get(name=college.lower())
            
        except:
            coll=None
        dajax.script('$("#register").modal(\'hide\');')
        dajax.script('$("#login").show();')
        coll=College(name=college,city=city,state=state)
        coll.save()
        dajax.assign("#add_coll_name",'innerHTML','%s'% college)
        dajax.assign("#add_coll_result",'innerHTML','Added your college:')
        dajax.script('$.bootstrapGrowl("Your college:<strong>%s</strong> was added. Welcome", {type:"success",timeout:12000} );'% str(coll.name) )
        # : populate the id_college with the given college details?
        dajax.script("$('#add_coll_message').toggle();")
        dajax.script("$('#form_registration #id_college').toggle();")
        dajax.script("$('#add_coll_form').toggle();")
#    colllist=College.objects.all()
    return dajax.json()

@dajaxice_register
def logout(request,**kwargs):
    dajax = Dajax()
    auth_logout(request)
    dajax.script('$.bootstrapGrowl("Successfully logged out!", {type:"success",timeout:12000} );' )
    dajax.assign("#login_logout", "innerHTML", '<a href="#login" onclick="$(\'#login\').modal(\'show\');">Login | Register </a>')
    return dajax.json()

@dajaxice_register
def login(request,login_form = None):
    dajax = Dajax()
    if request.user.is_authenticated():
        msg_login='%s, You are logged in!!' % request.user.username
        dajax.script('$.bootstrapGrowl("%s", {type:"danger",delay:20000} );'% msg_login )
        dajax.script('$(".modal-header").find(".close").click()')
        return dajax.json()
    elif request.method == 'POST' or login_form != None:
        form = LoginForm(deserialize_form(login_form))
        if form.is_valid() :
            data=form.cleaned_data
            username=data['username']
            password=data['password']
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    msg = 'Please click the activation link sent to your registered email id to activate your account'
                    dajax.script('$.bootstrapGrowl("%s", {type:"danger",timeout:12000} );' % msg)
                    dajax.script("$('#login_form #id_password').val('');")
                    return dajax.json()
                auth_login(request, user)
                dajax.script('$.bootstrapGrowl("Hi %s" , {type:"success",timeout:12000} );'% user.username )
                dajax.script("$('#login_form #id_password').val('');")
                dajax.script("$('#login').modal('hide');")
                dajax.script('$(".modal-header").find(".close").click()')
                dajax.assign("#login_logout", "innerHTML", '<a onclick="Dajaxice.users.logout(Dajax.process,{});" style="cursor:pointer;">Logout </a>')
                #display logout| edit profile on navbar

                return dajax.json()
            else:
                msg = 'Username and Password does not match!!!'
                if User.objects.filter(username=username).count()==0:
                    msg = 'Username not created, did you want to register?'
                dajax.script('$.bootstrapGrowl("%s", {type:"danger",timeout:12000} );' % msg)
                dajax.script("$('#login_form #id_password').val('');")
                form = LoginForm()
                form_registration = AddUserForm()
                return dajax.json()
        else:
            dajax.remove_css_class('#my_form input', 'error')
            for error in form.errors:
                dajax.add_css_class('#login_form #id_%s' % error, 'error')
            return dajax.json()
            #Code for error rendering
    else:
        dajax.script('$.bootstrapGrowl("Fill in required details", {type:"danger",timeout:12000} );')
        #empty form case
        return dajax.json()
    return dajax.json()

@dajaxice_register
def register(request,form_registration=None,college_name=None):
    #logged in user cannot register, but just in case
    dajax = Dajax()
    college = None
    new_coll = False
    if not college_name is None:
        try:
            college=College.objects.filter(name=str(college_name))[0]
            new_coll = True
        except:
            #impossible scenario!!
            dajax.alert('You must have entered your college first!')
            return dajax.json()
    
    if request.user.is_authenticated():
        msg_login = '%s, You are already logged in!!' % request.user.username
        dajax.script('$.bootstrapGrowl("Hi %s" , {type:"danger",timeout:12000} );'% msg_login )
        return dajax.json()
        
    if request.method=="POST" and (form_registration !=None or not college_name is None) :
        form = AddUserForm(deserialize_form(form_registration))
        if form.is_valid():
            #TODO: if we change college to be a compulsory, then this must be changed
#            dajax.remove_css_class('#form_registration input', 'error')
            data = form.cleaned_data
            new_user = User(first_name=data['first_name'],last_name=data['last_name'], username=data['username'], email=data['email'])
            new_user.set_password(data['password']) 
            new_user.save()
            new_user.is_active = False
            new_user.save()
            x = 1300000 + new_user.id 
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt + new_user.username).hexdigest()
            if college is None:
                userprofile = UserProfile(user=new_user,activation_key=activation_key,gender=data['gender'],age=data['age'],branch=data['branch'],mobile_number=data['mobile_number'],college=data['college'],college_roll=data['college_roll'],shaastra_id= ("SHA" + str(x)),key_expires = timezone.now()+datetime.timedelta(2))
            else:
                userprofile = UserProfile(user=new_user,activation_key=activation_key,gender=data['gender'],age=data['age'],branch=data['branch'],mobile_number=data['mobile_number'],college=college,college_roll=data['college_roll'],shaastra_id= ("SHA" + str(x)),key_expires = timezone.now()+datetime.timedelta(2))
            userprofile.save()
            mail_template = get_template('email/activate.html')
            body = mail_template.render( Context( {
                    'username':new_user.username,
                    'activationkey':userprofile.activation_key,
                    'SITE_URL':settings.SITE_URL,
                    'shaastra_id':userprofile.shaastra_id,
                }))
            dajax.script("$('#form_registration #id_password').val('');")
            dajax.script("$('#form_registration #id_password_again').val('');")
            dajax.script("$('#form_registration #id_phone_number').val('');")

            send_mail('Your new Shaastra2013 account confirmation', body,'noreply@shaastra.org', [new_user.email,], fail_silently=False)
            msg='A mail has been sent to the mail id u provided. Please activate your account within 48 hours. Please also check your spam folder'
            dajax.script('$(".modal-header").find(".close").click()')
            dajax.script('$.bootstrapGrowl("Hi %s" , {type:"success",timeout:12000} );'% msg )

            return dajax.json()
        else:
            errdict=dict()
            errdict=form.errors
            for error in form.errors:
                print error,errdict[error]
            dajax.script("$('#form_registration #id_password').val('');")
            dajax.script("$('#form_registration #id_password_again').val('');")
            for error in form.errors:
                dajax.add_css_class('#form_registration #id_%s' % error, 'error')
            dajax.script('$.bootstrapGrowl("Oops : There were errors when you tried to register !", {type:"danger",timeout:12000} );' )
            return dajax.json()
    if request.method == 'GET':
        form_registration = AddUserForm()
        return dajax.json()
    form_registration=AddUserForm()
    return dajax.json()


@dajaxice_register
def forgot_password(request,email=None):
    dajax = Dajax()
    if not email is None and not email == '' :
        try:
            validate_email(email)
#            validate_email is a django inbuilt function that throws ValidationError for wrong email address
#            Issue: starts with _ not acceptable
            profile = UserProfile.objects.get(user__email = str(email))
            email = profile.user.email
            user = profile.user
            mail_template = get_template('email/forgot_password.html')
            body = mail_template.render( Context( {
                    'username':user.username,
                    'SITE_URL':settings.SITE_URL,
                    'passwordkey':profile.activation_key,
                }))
            send_mail('Shaastra2013 password reset request', body,'noreply@shaastra.org', [user.email,], fail_silently=False)
            dajax.script('$.bootstrapGrowl("An email with a link to reset your password has been sent to your email id%s", {type:"success",timeout:12000} );' % email)
            dajax.script('$.bootstrapGrowl("Please also check your spam", {type:"danger",timeout:12000} );')
        except ValidationError:
            dajax.script('$.bootstrapGrowl("Your email:%s is invalid", {type:"danger",timeout:12000} );' % email)
            return dajax.json()
        except:
            dajax.script('$.bootstrapGrowl("Not a registered email id", {type:"danger",timeout:12000} );')
            return dajax.json()
    dajax.script('$.bootstrapGrowl("Enter your email id!", {type:"danger",timeout:12000} );')
    return dajax.json()

