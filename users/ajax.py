from django.utils import simplejson
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
from django.dispatch import receiver
from django.db.models.signals import post_save
from users.models import *
'''
@dajaxice_register
def alerter(request,**kwargs):
    print 'sssssssssssssssssss\n\n\n\n\n'
    dajax=Dajax()
    try:
        col=College(name=text1,city=text2,state=text3)
        col.save()
        #form['college']=col
    except:
        col=College.objects.get(name=text1)
        dajax.alert("Your college is already present")
    
    #return dajax.json()
    return simplejson.dumps({'message':'Added your college:: %s'% text1,'col':col})
'''
'''
@dajaxice_register
def college_form(request,data):
    print 'blah'
    dajax=Dajax()
    html_content='blahblah'
    dajax.alert(html_content)
    #dajax.assign('','innerHTML', html_content)
    return dajax.json()
'''

