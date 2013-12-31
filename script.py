from participantPDF_2k14 import *

uidlist = [up.user.id for up in UserProfile.objects.all() if up.get_regd_events()]
ct = 0
faillist = []
uid_faillist = []
for uid in uidlist:
 
    faillist.append(generatePDFs(uid))
    log("PDF generated for :%s\n" % uid)
    
