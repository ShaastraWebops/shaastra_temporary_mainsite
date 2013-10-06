from users.models import *
import sha,random
def populate_coll():
    str1='1234567890'
    str2='abcdefghij'
    str3='6544566546'
    for i in range(len(str1)):
        coll=College(name=str1[i],city=str2[i],state=str3[i])
        coll.save()
    return
    

def populate_up():
    s = '_participant'
    if College.objects.all().count() == 0:
        populate_coll()
    for i in range(100,111):
        try:
            u = User.objects.create_user(email = '%d@%s.com' % (i,s),username = s+str(i),password = '%s%d' % (s,i))
            u.first_name = '%s%d' % (s,i)
            u.last_name = str(i)
            u.save()
            u.is_active = False
            u.save()
        except:
            u=User.objects.get(email = '%d%s.com' % (i,s))
            if UserProfile.objects.get(user=u):
                print u.username
                return
        x = 1300000 + u.id
        salt = sha.new(str(random.random())).hexdigest()[:5]
        activation_key = sha.new(salt + u.username).hexdigest()
        userprofile = UserProfile(user=u,activation_key=activation_key,gender='M',age=18+i,branch='Mech',mobile_number=(int)('94439992%d%d' % (i,i+1)),college = College.objects.all()[0],college_roll='ROLL%d'% i,shaastra_id= ("SHA" + str(x)))
        userprofile.save()
        
    return
