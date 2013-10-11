import csv
from django.contrib.auth.models     import User, Group
from shaastra_temporary_mainsite u sers.models               import UserProfile
#from nss.mailer.nssmailer           import nss_send_mail
def csvread():

    rdr = csv.DictReader(open('users/total_team.csv','rb'),delimiter=',')
    username = []
    roll = []
    mobile = []
    email = []


    for d in rdr:
        username.append(d['username'])
        roll.append(d['roll'])
        mobile.append((d['mobile']))
        email.append(d['email'])
        i = 0
        while i<len(roll):

            unique_id = roll[i]
            username = roll[i]
            password = mobile[i]
            mail = email[i]
            if UserProfile.objects.all().filter(unique_id = roll[i]):
                print i
                userp = UserProfile.objects.all().get(unique_id = roll[i])
                userp.user.is_active = True
                if not userp.is_managerial():
                    if userp.is_vol():
                        userp.user.groups.remove(9)
                        userp.user.groups.add(1)
                    elif userp.is_project_rep():
                        userp.user.groups.add(1)
                    else:
                        userp.user.groups.add(1)
                        userp.user.save()
                        userp.save()
                else:
                    #print '%d @@@' % i
                    user = User.objects.create_user(username = username , email = mail , password = password)
                    user.is_active = True
                    user.save()

            userp = UserProfile.objects.create(user = user , unique_id = unique_id)
            userp.user.groups.add(1)
            userp.user.save()
            userp.save()
            i+=1
#csvread()              

