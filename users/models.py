#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings
import os,datetime
from django.utils import timezone
from dashboard.models import TeamEvent
BRANCH_CHOICES = (
    ('Arts', 'Arts'),
    ('Accounting', 'Accounting'),
    ('Applied Mechanics', 'Applied Mechanics'),
    ('Mechatronics', 'Mechatronics'),
    ('Aerospace Engineering', 'Aerospace Engineering'),
    ('Automobile Engineering', 'Automobile Engineering'),
    ('Biotech / Biochemical / Biomedical', 'Biotech / Biochemical / Biomedical'),
    ('Biology', 'Biology'),
    ('Ceramic Engineering', 'Ceramic Engineering'),
    ('Chemical Engineering', 'Chemical Engineering'),
    ('Chemistry', 'Chemistry'),
    ('Design', 'Design'),
    ('Engineering Design', 'Engineering Design'),
    ('Civil Engineering', 'Civil Engineering'),
    ('Computer Science and Engineering', 'Computer Science and Engineering'),
    ('Electronics and Communications Engineering', 'Electronics and Communications Engineering'),
    ('Electrical and Electronics Engineering', 'Electrical and Electronics Engineering'),
    ('Electrical Engineering', 'Electrical Engineering'),
    ('Electronics and Instrumentation Engineering', 'Electronics and Instrumentation Engineering'),
    ('Engineering Physics', 'Engineering Physics'),
    ('Economics', 'Economics'),
    ('Fashion Technology', 'Fashion Technology'),
    ('Humanities and Social Sciences', 'Humanities and Social Sciences'),
    ('Industrial Production', 'Industrial Production'),
    ('Production', 'Production'),
    ('Information Technology and Information Science', 'Information Technology and Sciences'),
    ('Management', 'Management'),
    ('Manufacturing', 'Manufacturing'),
    ('Mathematics', 'Mathematics'),
    ('Metallurgy and Material Science', 'Metallurgy and Material Science'),
    ('Mechanical Engineering', 'Mechanical Engineering'),
    ('Ocean Engineering and Naval Architecture', 'Ocean Engineering and Naval Architecture'),
    ('Physics', 'Physics'),
    ('Telecom', 'Telecom'),
    ('Textile Engineering', 'Textile Engineering'),
    ('Others', 'Others'),
)

#from events.models import Event
def upload_handler(model_name):
    def upload_func(instance, filename):
        return os.path.join(model_name, instance.title, filename)
    return upload_func
BRANCH_CHOICES = (
    ('Arts', 'Arts'),
    ('Accounting', 'Accounting'),
    ('Applied Mechanics', 'Applied Mechanics'),
    ('Mechatronics', 'Mechatronics'),
    ('Aerospace Engineering', 'Aerospace Engineering'),
    ('Automobile Engineering', 'Automobile Engineering'),
    ('Biotech / Biochemical / Biomedical', 'Biotech / Biochemical / Biomedical'),
    ('Biology', 'Biology'),
    ('Ceramic Engineering', 'Ceramic Engineering'),
    ('Chemical Engineering', 'Chemical Engineering'),
    ('Chemistry', 'Chemistry'),
    ('Design', 'Design'),
    ('Engineering Design', 'Engineering Design'),
    ('Civil Engineering', 'Civil Engineering'),
    ('Computer Science and Engineering', 'Computer Science and Engineering'),
    ('Electronics and Communications Engineering', 'Electronics and Communications Engineering'),
    ('Electrical and Electronics Engineering', 'Electrical and Electronics Engineering'),
    ('Electrical Engineering', 'Electrical Engineering'),
    ('Electronics and Instrumentation Engineering', 'Electronics and Instrumentation Engineering'),
    ('Engineering Physics', 'Engineering Physics'),
    ('Economics', 'Economics'),
    ('Fashion Technology', 'Fashion Technology'),
    ('Humanities and Social Sciences', 'Humanities and Social Sciences'),
    ('Industrial Production', 'Industrial Production'),
    ('Production', 'Production'),
    ('Information Technology and Information Science', 'Information Technology and Sciences'),
    ('Management', 'Management'),
    ('Manufacturing', 'Manufacturing'),
    ('Mathematics', 'Mathematics'),
    ('Metallurgy and Material Science', 'Metallurgy and Material Science'),
    ('Mechanical Engineering', 'Mechanical Engineering'),
    ('Ocean Engineering and Naval Architecture', 'Ocean Engineering and Naval Architecture'),
    ('Physics', 'Physics'),
    ('Telecom', 'Telecom'),
    ('Textile Engineering', 'Textile Engineering'),
    ('Others', 'Others'),
)

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

STATE_CHOICES = (
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu And Kashmir', 'Jammu And Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Orissa', 'Orissa'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman And Nicobar Islands', 'Andaman And Nicobar Islands'),
    ('Chandigarh', 'Chandigarh'),
    ('Dadra And Nagar Haveli', 'Dadra And Nagar Haveli'),
    ('Daman And Diu', 'Daman And Diu'),
    ('Lakshadweep', 'Lakshadweep'),
    ('NCT/Delhi', 'NCT/Delhi'),
    ('Puducherry', 'Puducherry'),
    ('Outside India', 'Outside India'),
)
class College(models.Model):

    name = models.CharField(max_length=255,
                            help_text='The name of your college. Please refrain from using short forms.'
                            )
    city = models.CharField(max_length=30,
                            help_text='The name of the city where your college is located. Please refrain from using short forms.'
                            )
    state = models.CharField(max_length=40, choices=STATE_CHOICES,
                             help_text='The state where your college is located. Select from the drop down list'
                             )

    def __unicode__(self):
        return '%s, %s, %s' % (self.name, self.city, self.state)

    class Admin:

        pass

class UserProfile(models.Model):

    user               = models.ForeignKey(User, unique=True)
    gender             = models.CharField(max_length=1, choices=GENDER_CHOICES,
                              default='F')  # Defaults to 'girl' ;-)
    age                = models.IntegerField(default=18)
                              # help_text='You need to be over 12 and under 80 years of age to participate'
                              # No age limit now.
    branch             = models.CharField(max_length=50, choices=BRANCH_CHOICES,
                              help_text='Your branch of study')
    mobile_number      = models.CharField(max_length=15, blank=True, null=True,
                              help_text='Please enter your current mobile number')
    college            = models.ForeignKey(College, null=True, blank=True)
    college_roll       = models.CharField(max_length=40, null=True)

    shaastra_id        = models.CharField(max_length = 20, unique = True, null=True)

    activation_key     = models.CharField(max_length=40, null=True)
    key_expires        = models.DateTimeField(default = timezone.now()+datetime.timedelta(2))
    want_accomodation  = models.BooleanField(default=False, help_text = "Doesn't assure accommodation during Shaastra.")
    school_student    = models.BooleanField(default=False)
    is_core = models.BooleanField(default=False)
    is_hospi = models.BooleanField(default=False)

#    facebook_id = models.CharField(max_length=20)
#    access_token = models.CharField(max_length=250)
    def save(self, *args, **kwargs):
        self.user.save()
        super(UserProfile, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.user.delete()
        super(UserProfile, self).delete(*args, **kwargs)
    
    def __unicode__(self):
        return self.user.first_name
    
    def get_regd_events(self):
        tevlist = []
        tevlist=TeamEvent.objects.filter(users__username=self.user.username)
        return tevlist
    class Admin:
        pass


    
class shows_updates(models.Model):
    shows_name = models.CharField(max_length=255,
                            help_text='Name of the Show'
                            )
    update    = models.CharField(max_length=255,help_text='Update field')
    def __unicode__(self):
        return '%s  %s'%(self.show_name,self.update)
    class meta:
        ordering=['-id']
        
EVENT_CATEGORIES = (
    ('Aerofest', 'Aerofest'),
    ('Coding', 'Coding'),
    ('Design and Build', 'Design and Build'),
    ('Involve', 'Involve'),
    ('Quizzes', 'Quizzes'),
    ('Online', 'Online'),
    ('Department Flagship', 'Department Flagship'),
    ('Spotlight', 'Spotlight'),
    ('Workshops', 'Workshops'),
    ('Exhibitions', 'Exhibitions and Shows'),
    ('Associated Events', 'Associated Events'),
    ('Sampark', 'Sampark'),
    )

UPDATE_CATEGORY = (
    ('Major Update', 'Major Update'),
    ('Updates', 'Updates'),
    )

class Tag(models.Model):
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name

class SponsLogoUploads(models.Model):
    logo1 = models.FileField(upload_to=upload_handler('sponslogo'), blank=True, null=True)
    logo2 = models.FileField(upload_to=upload_handler('sponslogo'), blank=True, null=True)
    logo3 = models.FileField(upload_to=upload_handler('sponslogo'), blank=True, null=True)
    #more fields to be added when max number of uploads is known

