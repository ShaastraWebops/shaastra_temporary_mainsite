#from participantPDF_2k14 import *
import os

from django.conf import settings
#from mainsite_2014 import settings as bulkset
import sys
import os
sys.path.append('/home/shaastra/django-projects/Shaastra-2014/mainsite')
sys.path.append('/home/shaastra/django-projects/Shaastra-2014')
sys.path.append('/home/shaastra/django-projects/Shaastra-2014/mainsite/mainsite_2014')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mainsite_2014.settings'
#settings.configure(bulkset,DEBUG=True, TEMPLATE_DEBUG=True)
from participantPDF_2k14 import *

uidlist = [up.user.id for up in UserProfile.objects.all().order_by('shaastra_id')]
ct = 0
faillist = []
uid_faillist = []
for uid in uidlist:
 
    faillist.append(generatePDFs(uid))
    log("PDF generated for :%s\n" % uid)
    
