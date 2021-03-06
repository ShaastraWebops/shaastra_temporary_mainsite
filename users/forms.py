from django import forms
from django.forms import ModelForm
from django.db import models as d_models
from django.contrib.auth.models import User
from django.template import Template, Context
from django.utils.safestring import mark_safe
from users.models import *
#from django.core.validators import alnum_re

GENDER_CHOICES = ((1, 'Male'), (2, 'Female'))

class LoginForm(forms.Form):
    username = forms.CharField(help_text='Your Shaastra 2013 username')
    password = forms.CharField(widget=forms.PasswordInput,
                               help_text='Your password')

class ChangePasswordForm(forms.Form):
    
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_again = forms.CharField(widget=forms.PasswordInput)
    def clean_new_password(self):
        if self.prefix:
            field_name1 = '%s-new password' % self.prefix
            field_name2 = '%s-new password again' % self.prefix
        else:
            field_name1 = 'new_password'
            field_name2 = 'new_password_again'

        if self.data[field_name1] != '' and self.data[field_name1] != self.data[field_name2]:
            raise forms.ValidationError('The entered passwords do not match.')
        elif len(self.data[field_name1])<6:
            raise forms.ValidationError('Password minumum length is 6')
        else:
            return self.data[field_name1]
            
class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    password_again = forms.CharField(widget=forms.PasswordInput)
    def clean_password(self):
        if self.prefix:
            field_name1 = '%s-password' % self.prefix
            field_name2 = '%s-password_again' % self.prefix
        else:
            field_name1 = 'password'
            field_name2 = 'password_again'

        if self.data[field_name1] != '' and self.data[field_name1] \
            != self.data[field_name2]:
            raise forms.ValidationError('The entered passwords do not match.')
        elif len(self.data[field_name1])<6:
            raise forms.ValidationError('Password minumum length is 6')
        else:
            return self.data[field_name1]



    #errors=[]
class BaseUserForm(forms.ModelForm):

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:

        model = UserProfile

    # The following code is to clean the a age field and to ensure that age is between 12 and 80.
    # Age limit has now been removed as demanded in Issue #29. To add it back, uncomment the 
    # following and also add the help_text in the age field in the model.
    '''
    def clean_age(self):
        if self.cleaned_data['age'] > 80 or self.cleaned_datlease enter your current mobile number
a['age'] \
            < 12:
            raise forms.ValidationError(u'<p>Please enter an acceptable age (12 to 80)</p>'
                    )
        else:
            return self.cleaned_data['age']
    '''
    
    def clean_mobile_number(self):
        if len(self.cleaned_data['mobile_number']) != 10 \
            or self.cleaned_data['mobile_number'][0] != '7' \
            and self.cleaned_data['mobile_number'][0] != '8' \
            and self.cleaned_data['mobile_number'][0] != '9' \
            or not self.cleaned_data['mobile_number'].isdigit():
            raise forms.ValidationError(u'<p>Enter a valid mobile number</p>'
                    )
        if UserProfile.objects.filter(mobile_number=self.cleaned_data['mobile_number'
                ]):
            pass
        else:
            return self.cleaned_data['mobile_number']
        raise forms.ValidationError('<p>This mobile number is already registered</p>'
                                    )

    def clean_first_name(self):
        if not self.cleaned_data['first_name'].replace(' ', ''
                ).isalpha():
            raise forms.ValidationError(u'<p>Names cannot contain anything other than alphabets.</p>'
                    )
        else:
            return self.cleaned_data['first_name']

    def clean_last_name(self):
        if not self.cleaned_data['last_name'].replace(' ', ''
                ).isalpha():
            raise forms.ValidationError(u'<p>Names cannot contain anything other than alphabets.</p>'
                    )
        else:
            return self.cleaned_data['last_name']

class AddUserForm(BaseUserForm):

    username = forms.CharField(max_length=30,
                               help_text='Please select a username.',
                               label='Shaastra username')
    email =forms.EmailField(help_text='Please enter a email_id')
    password = forms.CharField(min_length=6, max_length=30,
                               widget=forms.PasswordInput,
                               help_text='Passwords need to be atleast 6 characters long.'
                               )
    password_again = forms.CharField(max_length=30,
            widget=forms.PasswordInput,
            help_text='Enter the same password that you entered above')
    #gender = models.CharField(choices=GENDER_CHOICES,default='Female')  # Defaults to 'girl' ;-)

    #branch = chosenforms.ChosenChoiceField(overlay="You major in...", choices = BRANCH_CHOICES)
    #college = chosenforms.ChosenModelChoiceField(overlay="You study at...", queryset=College.objects.all())

    class Meta(BaseUserForm.Meta):
	model = UserProfile

        fields = (
            'last_name',
            'first_name',
            'username',
            'email',
            'password_again',
            'password',
            'college_roll',
            'gender',
            'branch',
            'age',
            'mobile_number',
            'want_accomodation',
            'college',
            'school_student'
            )

        # exclude = {'is_coord','coord_event','shaastra_id','activation_key','key_expires','UID','user',}

    def clean_username(self):
        #if not alnum_re.search(self.cleaned_data['username']):
        #   raise forms.ValidationError(u'Usernames can only contain letters, numbers and underscores'
        #            )
        if User.objects.filter(username=self.cleaned_data['username']):
            pass
        else:
            return self.cleaned_data['username']
        raise forms.ValidationError('This username is already taken. Please choose another.'
                                    )

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']):
            pass
        else:
            return self.cleaned_data['email']
        raise forms.ValidationError('This email address is already taken. Please choose another.'
                                    )

    def clean_password(self):
        if self.prefix:
            field_name1 = '%s-password' % self.prefix
            field_name2 = '%s-password_again' % self.prefix
        else:
            field_name1 = 'password'
            field_name2 = 'password_again'

        if self.data[field_name1] != '' and self.data[field_name1] \
            != self.data[field_name2]:
            raise forms.ValidationError('The entered passwords do not match.'
                    )
        else:
            return self.data[field_name1]
    def save(self):
        col=self.college
        super(self).save()

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('branch', 'college','mobile_number', 'college_roll','gender','age')

    def clean_mobile_number(self):
        number1 = self.cleaned_data['mobile_number']
        try:
            int(number1)
        except ValueError, e:
            raise forms.ValidationError ("Enter a valid number")
        if number1 == '':
            return number1
        elif ((len(number1)<9) or (len(number1)>15)):
            raise forms.ValidationError ("Enter a valid number")
        else :
            return self.data['mobile_number']
    
    class Admin:
        pass
        
class Feedback(forms.ModelForm):
	class Meta:
		model = feedbackmodel
		field=('comprehensive_rating','navigation_rating','theme_rating','how_came_rating','other_suggestion')
		
	

