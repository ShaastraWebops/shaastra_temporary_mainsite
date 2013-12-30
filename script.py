from participantPDF_2k14 import *

uidlist = [up.user.id for up in UserProfile.objects.all()]
ct = 0
faillist = []
uid_faillist = []
for uid in uidlist:
    try:
        faillist.append(generatePDFs(uid))
        log("PDF generated for :%s\n" % uid)
        
    except:
        ct = ct+1
        uid_faillist.append(uid)
