from participantPDF_2k14 import *



for profile in UserProfile.objects.all()[9670:]:
    try:
        generatePDFs(profile.user.id)
    except:
        print profile.shaastra_id
        log("failed in fn:%s"% profile.shaastra_id)
        
#for users in list::
#generatePDFs(user_id)

#needed: set location in /home/shaastra/hospi/..
