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
from django.template.loader import get_template
from django.shortcuts import render_to_response, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
#from events.models import Event
from django.utils.translation import ugettext as _
from django.contrib.sessions.models import Session
from misc.dajaxice.core import dajaxice_functions
from dashboard.models import TDPFileForm
from django.utils import simplejson
from misc.dajaxice.decorators import dajaxice_register
from django.dispatch import receiver
import datetime
from forms import EditProfileForm


@dajaxice_register
def edit_profile(request,form = None,first_name = None,last_name = None):
    dajax = Dajax()
    print deserialize_form(form)
    if form is None or first_name is None or last_name is None:
        dajax.script('$.bootstrapGrowl("Invalid edit profile request", {type:"danger",timeout:50000} );')
        return dajax.json()
    if first_name == '' or last_name == '':
        dajax.script('$.bootstrapGrowl("Empty first name/last name fields not allowed", {type:"danger",timeout:50000} );')
        return dajax.json()
    form = EditProfileForm(deserialize_form(form))
    if not form.is_valid():
        errdict = dict(form.errors)
        for error in form.errors:
#            if str(errdict[error][0])!='This field is required.':
            dajax.script('$.bootstrapGrowl("%s:: %s" , {type:"error",timeout:50000} );'% (str(error),str(errdict[error][0])))
        return dajax.json()
    profile = UserProfile.objects.get(user=request.user)
    (profile.branch,profile.mobile_number,profile.college_roll,profile.gender,profile.age)  = (form.cleaned_data['branch'],form.cleaned_data['mobile_number'],form.cleaned_data['college_roll'],form.cleaned_data['gender'],form.cleaned_data['age'])
    profile.user.first_name = first_name
    profile.user.last_name = last_name
    profile.save()
    print profile.user.first_name
    print profile.mobile_number
    dajax.script('$.bootstrapGrowl("Your profile has been edited" , {type:"success",timeout:100000,align:"center",width:"auto"} );')
    return dajax.json()

@dajaxice_register
def edit_profile_form(request):
    dajax = Dajax()
    print '********'
    print request.user.is_authenticated()
    #: if user has chosen a college in dropdown, depopulate it OR growl
    if not request.user.is_authenticated():
        dajax.script('$.bootstrapGrowl("Login First!", {type:"danger",timeout:50000} );')
        return dajax.json()
    else:
        profile = UserProfile.objects.get(user=request.user)
        edit_profile_form = EditProfileForm(instance = profile)
        context_dict = {'edit_profile_form':edit_profile_form,'profile':profile}
        html_stuff = render_to_string('dashboard/profile.html',context_dict,RequestContext(request))
        if html_stuff:
            dajax.assign('#FormRegd','innerHTML',html_stuff)
            dajax.script('$("#event_register").modal("show");')
    print '\\\\\\\\\\\\\\\\\\\\'
    return dajax.json()

@dajaxice_register
def submit_tdp(request,teamevent_id = None,file_tdp=None):
    dajax = Dajax()
    print 'file!!!!!!!!!!'
    if teamevent_id is None or file_tdp is None:
        dajax.script('$.bootstrapGrowl("Invalid TDP Upload request", {type:"danger",timeout:50000} );')
        return dajax.json()
    team_event =TeamEvent.objects.get(id = teamevent_id)
    if len(request.FILES) == 0:
        dajax.script('$.bootstrapGrowl("Please upload a file first!", {type:"danger",timeout:50000} );')
    fileform = TDPFileForm(deserialize_form(file_tdp),request.FILES)
    print request.raw_post_data
    try:
        event = teamevent.get_event()
        tdp = TDP(tdp=fileform,teamevent = teamevent)
        tdp.save()
    except:
        print 'sss'
    return dajax.json()
    
@dajaxice_register
def show_registered_events(request):
    dajax = Dajax()
    print '********'
    if not request.user.is_authenticated():
        dajax.script('$.bootstrapGrowl("Login to view your registered events", {type:"danger",timeout:50000} );')
        return dajax.json()
    else:
        profile = UserProfile.objects.get(user=request.user)
        team_event_list = profile.get_regd_events()
        no_regd = len(team_event_list)
        now = timezone.now()
        context_dict = {'team_event_list':team_event_list,'profile':profile,'now':now,'TDPFileForm':TDPFileForm(),'no_regd':no_regd}
        html_stuff = render_to_string('dashboard/registered_events.html',context_dict,RequestContext(request))
        if html_stuff:
            dajax.assign('#FormRegd','innerHTML',html_stuff)
            dajax.script('$("#event_register").modal("show");')
    print '\\\\\\\\\\\\\\\\\\\\'
    return dajax.json()


@dajaxice_register
def add_college(request,college=None,city=None,state=None):
    dajax = Dajax()
    #: if user has chosen a college in dropdown, depopulate it OR growl
    if city is None or college is None or state is None or city =='' or college =='' or state =='':
        dajax.script('$.bootstrapGrowl("Please enter relevant details for adding your college", {type:"danger",timeout:50000} );')
        return dajax.json()
    else:
        try:
            for coll in College.objects.all():
                if coll.name.lower() == college.lower():
                    dajax.script('$.bootstrapGrowl("Your college is already on our list, please check again", {type:"danger",timeout:50000} );')
                    return dajax.json()    
        except:
            coll=None
        dajax.script('$("#add_college").modal(\'hide\');')
        dajax.script('$("#login").show();')
        coll=College(name=college,city=city,state=state)
        coll.save()
        dajax.assign("#add_coll_name",'innerHTML','%s'% college)
        dajax.assign("#add_coll_result",'innerHTML','Added your college:')
        dajax.script('$.bootstrapGrowl("Your college:<strong>%s</strong> was added. Welcome", {type:"success",timeout:50000} );'% str(coll.name) )
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
    dajax.script('$.bootstrapGrowl("Successfully logged out!", {type:"success",timeout:50000} );' )
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
                    dajax.script('$.bootstrapGrowl("%s", {type:"danger",timeout:50000} );' % msg)
                    dajax.script("$('#login_form #id_password').val('');")
                    return dajax.json()
                auth_login(request, user)
                dajax.script('$.bootstrapGrowl("Hi %s" , {type:"success",timeout:50000} );'% user.username )
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
                dajax.script('$.bootstrapGrowl("%s", {type:"danger",timeout:50000} );' % msg)
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
        dajax.script('$.bootstrapGrowl("Fill in required details", {type:"danger",timeout:50000} );')
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
            dajax.script("$.bootstrapGrowl('You must have entered your college first!', {type:'danger',timeout:50000});")
            dajax.script('$("#gif_registration").hide();$("#form_registration_submit").show()')
    
            return dajax.json()
    
    if request.user.is_authenticated():
        msg_login = '%s, You are already logged in!!' % request.user.username
        dajax.script('$.bootstrapGrowl("Hi %s" , {type:"danger",timeout:50000} );'% msg_login )
        dajax.script('$("#gif_registration").hide();$("#form_registration_submit").show()')
    
        return dajax.json()
        
    if request.method=="POST" and (form_registration !=None or not college_name is None):
        form = AddUserForm(deserialize_form(form_registration))
        for error in form.errors:
            print error,form.errors[error]
        if form.is_valid():
            #TODO: if we change college to be a compulsory, then this must be changed
            dajax.remove_css_class('#form_registration input', 'error')
            data = form.cleaned_data
            new_user = User(first_name=data['first_name'],last_name=data['last_name'], username=data['username'], email=data['email'])
            new_user.set_password(data['password']) 
            new_user.save()
            new_user.is_active = False
            new_user.save()
            x = 1400000 + new_user.id 
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
            #TODO: empty the entire form!!
#            dajax.script("$('#form_registration').val('');")\
            dajax.script("$('#form_registration #id_email').val('');\
                         $('#form_registration #id_password').val('');\
                         $('#form_registration #id_password_again').val('');\
                         $('#form_registration #id_mobile_number').val('');")
#            send_mail('Your new Shaastra2014 account confirmation', body,'noreply@shaastra.org', [new_user.email,], fail_silently=False)
            msg='A mail has been sent to the mail id u provided. Please activate your account within 48 hours. Please also check your spam folder'
#            dajax.script('$(".modal-header").find(".close").click();')
            dajax.script('$.bootstrapGrowl("Hi %s" , {type:"success",timeout:50000} );'% msg )
            dajax.script('$("#gif_registration").hide();$("#form_registration_submit").show()')
    
            return dajax.json()
        else:
            errdict=dict(form.errors)
            dajax.script('$.bootstrapGrowl("Oops : Following errors cropped up when you tried to register !", {type:"danger",timeout:50000} );')
            for error in form.errors:
                if str(errdict[error][0])!='This field is required.':
                    dajax.script('$.bootstrapGrowl(" %s" , {type:"error",timeout:50000} );'% str(errdict[error][0]))
            dajax.script("$('#form_registration #id_password').val('');")
            dajax.script("$('#form_registration #id_password_again').val('');")
            for error in form.errors:
                dajax.add_css_class('#form_registration #id_%s' % error, 'error')
            dajax.script('$("#gif_registration").hide();$("#form_registration_submit").show()')
            return dajax.json()
    if request.method == 'GET':
        form_registration = AddUserForm()
        dajax.script('$("#gif_registration").hide();$("#form_registration_submit").show()')
        return dajax.json()
    form_registration=AddUserForm()
    dajax.script('$("#gif_registration").hide();$("#form_registration_submit").show()')
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
#            send_mail('Shaastra2014 password reset request', body,'noreply@shaastra.org', [user.email,], fail_silently=False)
            dajax.script('$.bootstrapGrowl("An email with a link to reset your password has been sent to your email id: %s", {type:"success",timeout:50000} );' % email)
            dajax.script('$.bootstrapGrowl("Please also check your spam", {type:"danger",timeout:50000} );')
        except ValidationError:
            dajax.script('$.bootstrapGrowl("Your email:%s is invalid", {type:"danger",timeout:50000} );' % email)
            return dajax.json()
        except:
            dajax.script('$.bootstrapGrowl("Not a registered email id", {type:"danger",timeout:50000} );')
            return dajax.json()
    return dajax.json()

