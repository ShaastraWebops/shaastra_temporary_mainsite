from users.models import College
def populate_coll():
    str1='1234567890'
    str2='abcdefghij'
    str3='6544566546'
    for i in range(len(str1)):
        coll=College(name=str1[i],city=str2[i],state=str3[i])
        coll.save()
    return
