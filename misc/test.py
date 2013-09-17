from users.models import ERPUser, HOSTEL_CHOICES
from django.contrib.auth.models import User
from dept.models import Dept, Subdept
from tasks.models import Task, Comment
import datetime
import random
from events.models import GenericEvent, ParticipantEvent, AudienceEvent, Tab, EVENT_CATEGORIES

DEPT_RANGE = 5
SUBDEPT_RANGE = 5
CORE_RANGE = 5
COORD_RANGE = 25
SUPER_RANGE = 5
INTRATASK_ACCEPTED_RANGE = 20
INTRATASK_NEARLY_RANGE = 10
INTRATASK_REPORTED_RANGE = 5
INTRATASK_COMPLETED_RANGE = 2
CROSSTASK_UNACCEPTED_RANGE = 20
CROSSTASK_ACCEPTED_RANGE = 20
CROSSTASK_NEARLY_RANGE = 10
CROSSTASK_REPORTED_RANGE = 5
CROSSTASK_COMPLETED_RANGE = 2
PARTICIPANT_EVENT_RANGE = 5
AUDIENCE_EVENT_RANGE = 5
TAB_RANGE = 3


# _____________--- MAKE USERS ---______________#
def populate_db():
    # MAKE DEPARTMENTS
    print "Creating", DEPT_RANGE, "Departments"
    for i in range(DEPT_RANGE):
        if Dept.objects.filter(name="Dept" + str(i)).count():
            continue
        d = Dept()
        d.name = "Dept" + str(i)
        d.save()
    
    # MAKE SUB DEPTS
    print "Creating", SUBDEPT_RANGE, "Sub Departments"
    for d in Dept.objects.filter(name__startswith='Dept'):
        for i in range(SUBDEPT_RANGE):
            if Subdept.objects.filter(name="Subdept" + str(i) + " for " + d.name).count():
                continue
            sd = Subdept()
            sd.name = "Subdept" + str(i) + " for " + d.name
            sd.dept = d
            sd.save()
    
    # MAKE CORES
    print "Creating", CORE_RANGE, "Cores"
    for i in range(CORE_RANGE):
        if ERPUser.objects.filter(nickname="Corenick" + str(i)).count():
            continue
        u = ERPUser()
        if User.objects.filter(username = '_core'+str(i)).count(): # user doesnt exist
            u.user = User.objects.get(username = '_core'+str(i))
        else:
            u.user = User.objects.create_user(
                username = '_core'+str(i), 
                password = str(i)
            )
        u.user.username = '_core'+str(i)
        u.user.set_password(str(i))
        u.user.email = "core" + str(i) + "email@shaastra.org"
        u.user.first_name = "Core" + str(i)
        u.user.last_name = "ACore"
        if Dept.objects.filter(name="Dept"+str(i%DEPT_RANGE)).count():
            u.dept = Dept.objects.get(name="Dept"+str(i%DEPT_RANGE))
        else:
            print "Error, there is no dept to assign the core to"
            return
        u.status = 2
        u.nickname = "Corenick" + str(i)
        u.chennai_number = str(i%10)*10
        u.summer_number = str((i%100)/10)*10
        u.summer_stay = "full"
        u.hostel = HOSTEL_CHOICES[i%len(HOSTEL_CHOICES)][0]
        u.room_no = i%1000
        u.user.save()
        u.save()
        #INSTANCE MUST BE SAVED BEFORE MANY TO MANY RELATIONS CAN BE SET.
        u.core_relations.add(u.dept)
        u.save()
    
    # MAKE COORDS
    print "Creating", COORD_RANGE, "Coords"
    for i in range(COORD_RANGE):
        if ERPUser.objects.filter(nickname="Coordnick" + str(i)).count():
            continue
        u = ERPUser()
        if User.objects.filter(username = '_coord'+str(i)).count(): # user doesnt exist
            u.user = User.objects.get(username = '_coord'+str(i))
        else:
            u.user = User.objects.create_user(
                username = '_coord'+str(i), 
                password = str(i)
            )
        u.user.username = '_coord'+str(i)
        u.user.set_password(str(i))
        u.user.email = "coord" + str(i) + "email@shaastra.org"
        u.user.first_name = "Coord" + str(i)
        u.user.last_name = "ACoord"
        if Dept.objects.filter(name="Dept"+str(i%DEPT_RANGE)).count():
            u.dept = Dept.objects.get(name="Dept"+str(i%DEPT_RANGE))
        else:
            print "Error, there is no dept to assigns the coord to"
            return
        if Subdept.objects.filter(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + u.dept.name).count():
            u.subdept = Subdept.objects.get(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + u.dept.name)
        else:
            print "Error, there is no SUBdept to assign the coord to"
            return
        u.status = 0
        u.nickname = "Coordnick" + str(i)
        u.chennai_number = str(i%10)*10
        u.summer_number = str((i%100)/10)*10
        u.summer_stay = "full"
        u.hostel = HOSTEL_CHOICES[i%len(HOSTEL_CHOICES)][0]
        u.room_no = i%1000
        u.user.save()
        u.save()
        #INSTANCE MUST BE SAVED BEFORE MANY TO MANY RELATIONS CAN BE SET.
        u.coord_relations.add(u.subdept)
        u.save()
    
    # MAKE SUPERCOORDS
    print "Creating", SUPER_RANGE, "Supers"
    for i in range(SUPER_RANGE):
        if ERPUser.objects.filter(nickname="Supernick" + str(i)).count():
            continue
        u = ERPUser()
        if User.objects.filter(username = '_super'+str(i)).count(): # user doesnt exist
            u.user = User.objects.get(username = '_super'+str(i))
        else:
            u.user = User.objects.create_user(
                username = '_super'+str(i), 
                password = str(i)
            )
        u.user.username = '_super'+str(i)
        u.user.set_password(str(i))
        u.user.email = "super" + str(i) + "email@shaastra.org"  
        u.user.first_name = "Super" + str(i)
        u.user.last_name = "ASuper"
        if Dept.objects.filter(name="Dept"+str(i%DEPT_RANGE)).count():
            u.dept = Dept.objects.get(name="Dept"+str(i%DEPT_RANGE))
        else:
            print "Error, there is no dept to assign the super to"
            return
        u.status = 1
        u.nickname = "Supernick" + str(i)
        u.chennai_number = str(i%10)*10
        u.summer_number = str((i%100)/10)*10
        u.summer_stay = "full"
        u.hostel = HOSTEL_CHOICES[i%len(HOSTEL_CHOICES)][0]
        u.room_no = i%1000
        u.user.save()
        u.save()
        #INSTANCE MUST BE SAVED BEFORE MANY TO MANY RELATIONS CAN BE SET.
        u.supercoord_relations.add(u.dept)
        u.save()
        
    
    # MAKE INTRA DEPARTMENTAL TASKS - ACCEPTED
    print "Creating", INTRATASK_ACCEPTED_RANGE, "Intra dept tasks which are ACCEPTED"
    for i in range(INTRATASK_ACCEPTED_RANGE):
        if Task.objects.filter(subject="Subject for Intra approved Task" + str(i)).count():
            continue
        t = Task()
        if ERPUser.objects.filter(nickname="Corenick" + str(i%CORE_RANGE) ).count() :
            t.taskcreator = ERPUser.objects.get(nickname="Corenick" + str(i%CORE_RANGE) )
        else : 
            print "Error, there is no user", "Corenick" + str(i%CORE_RANGE) , "to assign the task to"
            return
        t.deadline = datetime.date.today() # date is in datetime
        t.subject = "Subject for Intra approved Task" + str(i)
        t.description = "This a description for this Task. It is task number " + str(i) + "."
        if Dept.objects.filter(name="Dept" + str(int(i%DEPT_RANGE)) ).count() :
            t.origindept = Dept.objects.get(name="Dept" + str(int(i%DEPT_RANGE)) )
            t.targetdept = t.origindept
        else :
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        # Subdepts in origin dept
        if Subdept.objects.filter(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name ).count():
            t.targetsubdept = Subdept.objects.get(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name )
        else:
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        t.save()
        # Intra, So Taskforce if from origin dept only.
        if ERPUser.objects.filter(dept__name=t.origindept.name ).count():
            t.taskforce = ERPUser.objects.filter(dept__name=t.origindept.name )
        else:
            print "Error, there is no taskforce in dept", t.origindept.name , "to assign the task to"
            return
        t.isxdepartmental = False
        t.taskstatus = 'O'
        t.save()
    
    # MAKE INTRA DEPARTMENTAL TASKS - NEARLY COMPLETE
    print "Creating", INTRATASK_NEARLY_RANGE, "Intra dept tasks which are NEARLY COMPLETED"
    for i in range(INTRATASK_NEARLY_RANGE):
        if Task.objects.filter(subject="Subject for Intra almost_complete Task" + str(i)).count():
            continue
        t = Task()
        if ERPUser.objects.filter(nickname="Corenick" + str(i%CORE_RANGE) ).count() :
            t.taskcreator = ERPUser.objects.get(nickname="Corenick" + str(i%CORE_RANGE) )
        else : 
            print "Error, there is no user", "Corenick" + str(i%CORE_RANGE) , "to assign the task to"
            return
        t.deadline = datetime.date.today() # date is in datetime
        t.subject = "Subject for Intre almost_complete Task" + str(i)
        t.description = "This a description for this Task. It is task number " + str(i) + "."
        if Dept.objects.filter(name="Dept" + str(int(i%DEPT_RANGE)) ).count() :
            t.origindept = Dept.objects.get(name="Dept" + str(int(i%DEPT_RANGE)) )
            t.targetdept = t.origindept
        else :
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        # Subdepts in origin dept
        if Subdept.objects.filter(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name ).count():
            t.targetsubdept = Subdept.objects.get(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name )
        else:
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        t.save()
        # Intra, So Taskforce if from origin dept only.
        if ERPUser.objects.filter(dept__name=t.origindept.name ).count():
            t.taskforce = ERPUser.objects.filter(dept__name=t.origindept.name )
        else:
            print "Error, there is no taskforce in dept", t.origindept.name , "to assign the task to"
            return
        t.isxdepartmental = False
        t.taskstatus = 'A'
        t.save()
    
    # MAKE INTRA DEPARTMENTAL TASKS - REPORTED COMPLETE
    print "Creating", INTRATASK_REPORTED_RANGE, "Intra dept tasks which are REPORTED COMPLETED"
    for i in range(INTRATASK_REPORTED_RANGE):
        if Task.objects.filter(subject="Subject for Intra reported_completed Task" + str(i)).count():
            continue
        t = Task()
        if ERPUser.objects.filter(nickname="Corenick" + str(i%CORE_RANGE) ).count() :
            t.taskcreator = ERPUser.objects.get(nickname="Corenick" + str(i%CORE_RANGE) )
        else : 
            print "Error, there is no user", "Corenick" + str(i%CORE_RANGE) , "to assign the task to"
            return
        t.deadline = datetime.date.today() # date is in datetime
        t.subject = "Subject for Intra reported_completed Task" + str(i)
        t.description = "This a description for this Task. It is task number " + str(i) + "."
        if Dept.objects.filter(name="Dept" + str(int(i%DEPT_RANGE)) ).count() :
            t.origindept = Dept.objects.get(name="Dept" + str(int(i%DEPT_RANGE)) )
            t.targetdept = t.origindept
        else :
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        # Subdepts in origin dept
        if Subdept.objects.filter(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name ).count():
            t.targetsubdept = Subdept.objects.get(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name )
        else:
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        t.save()
        # Intra, So Taskforce if from origin dept only.
        if ERPUser.objects.filter(dept__name=t.origindept.name ).count():
            t.taskforce = ERPUser.objects.filter(dept__name=t.origindept.name )
        else:
            print "Error, there is no taskforce in dept", t.origindept.name , "to assign the task to"
            return
        t.isxdepartmental = False
        t.taskstatus = 'R'
        t.save()
    
    # MAKE INTRA DEPARTMENTAL TASKS - COMPLETED
    print "Creating", INTRATASK_COMPLETED_RANGE, "Intra dept tasks which are COMPLETED"
    for i in range(INTRATASK_COMPLETED_RANGE):
        if Task.objects.filter(subject="Subject for Intra completed Task" + str(i)).count():
            continue
        t = Task()
        if ERPUser.objects.filter(nickname="Corenick" + str(i%CORE_RANGE) ).count() :
            t.taskcreator = ERPUser.objects.get(nickname="Corenick" + str(i%CORE_RANGE) )
        else : 
            print "Error, there is no user", "Corenick" + str(i%CORE_RANGE) , "to assign the task to"
            return
        t.deadline = datetime.date.today() # date is in datetime
        t.subject = "Subject for Intra completed Task" + str(i)
        t.description = "This a description for this Task. It is task number " + str(i) + "."
        if Dept.objects.filter(name="Dept" + str(int(i%DEPT_RANGE)) ).count() :
            t.origindept = Dept.objects.get(name="Dept" + str(int(i%DEPT_RANGE)) )
            t.targetdept = t.origindept
        else :
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        # Subdepts in origin dept
        if Subdept.objects.filter(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name ).count():
            t.targetsubdept = Subdept.objects.get(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name )
        else:
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        t.save()
        # Intra, So Taskforce if from origin dept only.
        if ERPUser.objects.filter(dept__name=t.origindept.name ).count():
            t.taskforce = ERPUser.objects.filter(dept__name=t.origindept.name )
        else:
            print "Error, there is no taskforce in dept", t.origindept.name , "to assign the task to"
            return
        t.isxdepartmental = False
        t.taskstatus = 'C'
        t.save()
    
    # MAKE CROSS DEPARTMENTAL TASKS - UNACCEPTED
    print "Creating", CROSSTASK_UNACCEPTED_RANGE, "Cross dept tasks which are UNAPPROVED"
    for i in range(CROSSTASK_UNACCEPTED_RANGE):
        if Task.objects.filter(subject="Subject for Cross unapproved Task" + str(i)).count():
            continue
        t = Task()
        if ERPUser.objects.filter(nickname="Corenick" + str(i%CORE_RANGE) ).count() :
            t.taskcreator = ERPUser.objects.get(nickname="Corenick" + str(i%CORE_RANGE) )
        else : 
            print "Error, there is no user", "Corenick" + str(i%CORE_RANGE) , "to assign the task to"
            return
        t.deadline = datetime.date.today() # date is in datetime
        t.subject = "Subject for Cross unapproved Task" + str(i)
        t.description = "This a description for this Task. It is task number " + str(i) + "."
        if Dept.objects.filter(name="Dept" + str(int(i%DEPT_RANGE)) ).count() :
            t.origindept = Dept.objects.get(name="Dept" + str(int(i%DEPT_RANGE)) )
            # get a random target dept
            t.targetdept = Dept.objects.get(name="Dept" + str(int((i+random.randint(1, DEPT_RANGE-1))%DEPT_RANGE)) )
        else :
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        # Subdepts in origin dept
        if Subdept.objects.filter(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name ).count():
            t.targetsubdept = Subdept.objects.get(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name )
        else:
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        t.save()
        # Intra, So Taskforce if from origin dept only.
        if ERPUser.objects.filter(dept__name=t.origindept.name ).count():
            t.taskforce = ERPUser.objects.filter(dept__name=t.origindept.name )
        else:
            print "Error, there is no taskforce in dept", t.origindept.name , "to assign the task to"
            return
        t.isxdepartmental = True
        t.taskstatus = 'U'
        t.save()
    
    # MAKE CROSS DEPARTMENTAL TASKS - ACCEPTED
    print "Creating", CROSSTASK_ACCEPTED_RANGE, "Cross dept tasks which are APPROVED"
    for i in range(CROSSTASK_ACCEPTED_RANGE):
        if Task.objects.filter(subject="Subject for Cross approved Task" + str(i)).count():
            continue
        t = Task()
        if ERPUser.objects.filter(nickname="Corenick" + str(i%CORE_RANGE) ).count() :
            t.taskcreator = ERPUser.objects.get(nickname="Corenick" + str(i%CORE_RANGE) )
        else : 
            print "Error, there is no user", "Corenick" + str(i%CORE_RANGE) , "to assign the task to"
            return
        t.deadline = datetime.date.today() # date is in datetime
        t.subject = "Subject for Cross approved Task" + str(i)
        t.description = "This a description for this Task. It is task number " + str(i) + "."
        if Dept.objects.filter(name="Dept" + str(int(i%DEPT_RANGE)) ).count() :
            t.origindept = Dept.objects.get(name="Dept" + str(int(i%DEPT_RANGE)) )
            # get a random target dept
            t.targetdept = Dept.objects.get(name="Dept" + str(int((i+random.randint(1, DEPT_RANGE-1))%DEPT_RANGE)) )
        else :
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        # Subdepts in origin dept
        if Subdept.objects.filter(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name ).count():
            t.targetsubdept = Subdept.objects.get(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name )
        else:
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        t.save()
        # Intra, So Taskforce if from origin dept only.
        if ERPUser.objects.filter(dept__name=t.origindept.name ).count():
            t.taskforce = ERPUser.objects.filter(dept__name=t.origindept.name )
        else:
            print "Error, there is no taskforce in dept", t.origindept.name , "to assign the task to"
            return
        t.isxdepartmental = True
        t.taskstatus = 'O'
        t.save()
    
    # MAKE CROSS DEPARTMENTAL TASKS - NEARLY COMPLETE
    print "Creating", CROSSTASK_NEARLY_RANGE, "Cross dept tasks which are NEARLY COMPLETE"
    for i in range(CROSSTASK_NEARLY_RANGE):
        if Task.objects.filter(subject="Subject for Cross almost_completed Task" + str(i)).count():
            continue
        t = Task()
        if ERPUser.objects.filter(nickname="Corenick" + str(i%CORE_RANGE) ).count() :
            t.taskcreator = ERPUser.objects.get(nickname="Corenick" + str(i%CORE_RANGE) )
        else : 
            print "Error, there is no user", "Corenick" + str(i%CORE_RANGE) , "to assign the task to"
            return
        t.deadline = datetime.date.today() # date is in datetime
        t.subject = "Subject for Cross almost_completed Task" + str(i)
        t.description = "This a description for this Task. It is task number " + str(i) + "."
        if Dept.objects.filter(name="Dept" + str(int(i%DEPT_RANGE)) ).count() :
            t.origindept = Dept.objects.get(name="Dept" + str(int(i%DEPT_RANGE)) )
            # get a random target dept
            t.targetdept = Dept.objects.get(name="Dept" + str(int((i+random.randint(1, DEPT_RANGE-1))%DEPT_RANGE)) )
        else :
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        # Subdepts in origin dept
        if Subdept.objects.filter(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name ).count():
            t.targetsubdept = Subdept.objects.get(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name )
        else:
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        t.save()
        # Intra, So Taskforce if from origin dept only.
        if ERPUser.objects.filter(dept__name=t.origindept.name ).count():
            t.taskforce = ERPUser.objects.filter(dept__name=t.origindept.name )
        else:
            print "Error, there is no taskforce in dept", t.origindept.name , "to assign the task to"
            return
        t.isxdepartmental = True
        t.taskstatus = 'A'
        t.save()
    
    # MAKE CROSS DEPARTMENTAL TASKS - REPORTED COMPLETE
    print "Creating", CROSSTASK_REPORTED_RANGE, "Cross dept tasks which are REPORTED COMPLETED"
    for i in range(CROSSTASK_REPORTED_RANGE):
        if Task.objects.filter(subject="Subject for Cross reported_completed Task" + str(i)).count():
            continue
        t = Task()
        if ERPUser.objects.filter(nickname="Corenick" + str(i%CORE_RANGE) ).count() :
            t.taskcreator = ERPUser.objects.get(nickname="Corenick" + str(i%CORE_RANGE) )
        else : 
            print "Error, there is no user", "Corenick" + str(i%CORE_RANGE) , "to assign the task to"
            return
        t.deadline = datetime.date.today() # date is in datetime
        t.subject = "Subject for Cross reported_completed Task" + str(i)
        t.description = "This a description for this Task. It is task number " + str(i) + "."
        if Dept.objects.filter(name="Dept" + str(int(i%DEPT_RANGE)) ).count() :
            t.origindept = Dept.objects.get(name="Dept" + str(int(i%DEPT_RANGE)) )
            # get a random target dept
            t.targetdept = Dept.objects.get(name="Dept" + str(int((i+random.randint(1, DEPT_RANGE-1))%DEPT_RANGE)) )
        else :
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        # Subdepts in origin dept
        if Subdept.objects.filter(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name ).count():
            t.targetsubdept = Subdept.objects.get(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name )
        else:
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        t.save()
        # Intra, So Taskforce if from origin dept only.
        if ERPUser.objects.filter(dept__name=t.origindept.name ).count():
            t.taskforce = ERPUser.objects.filter(dept__name=t.origindept.name )
        else:
            print "Error, there is no taskforce in dept", t.origindept.name , "to assign the task to"
            return
        t.isxdepartmental = True
        t.taskstatus = 'R'
        t.save()
    
    # MAKE CROSS DEPARTMENTAL TASKS - COMPLETED
    print "Creating", CROSSTASK_COMPLETED_RANGE, "Cross dept tasks which are COMPLETED"
    for i in range(CROSSTASK_COMPLETED_RANGE):
        if Task.objects.filter(subject="Subject for Cross completed Task" + str(i)).count():
            continue
        t = Task()
        if ERPUser.objects.filter(nickname="Corenick" + str(i%CORE_RANGE) ).count() :
            t.taskcreator = ERPUser.objects.get(nickname="Corenick" + str(i%CORE_RANGE) )
        else : 
            print "Error, there is no user", "Corenick" + str(i%CORE_RANGE) , "to assign the task to"
            return
        t.deadline = datetime.date.today() # date is in datetime
        t.subject = "Subject for Cross completed Task" + str(i)
        t.description = "This a description for this Task. It is task number " + str(i) + "."
        if Dept.objects.filter(name="Dept" + str(int(i%DEPT_RANGE)) ).count() :
            t.origindept = Dept.objects.get(name="Dept" + str(int(i%DEPT_RANGE)) )
            # get a random target dept
            t.targetdept = Dept.objects.get(name="Dept" + str(int((i+random.randint(1, DEPT_RANGE-1))%DEPT_RANGE)) )
        else :
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        # Subdepts in origin dept
        if Subdept.objects.filter(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name ).count():
            t.targetsubdept = Subdept.objects.get(name="Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name )
        else:
            print "Error, there is no subdept", "Subdept" + str((i/DEPT_RANGE)%SUBDEPT_RANGE) + " for " + t.origindept.name , "to assign the task to"
            return
        t.save()
        # Intra, So Taskforce if from origin dept only.
        if ERPUser.objects.filter(dept__name=t.origindept.name ).count():
            t.taskforce = ERPUser.objects.filter(dept__name=t.origindept.name )
        else:
            print "Error, there is no taskforce in dept", t.origindept.name , "to assign the task to"
            return
        t.isxdepartmental = True
        t.taskstatus = 'C'
        t.save()
    


def populate_events_db():
    #Participant Events
    print "Creating", PARTICIPANT_EVENT_RANGE,"Registrable events"
    for i in range(PARTICIPANT_EVENT_RANGE):
        if ParticipantEvent.objects.filter(title="_PEvent" + str(i)).count():
            continue
        pe = ParticipantEvent()
        pe.title = "_PEvent" + str(i) #You will soon see why I started with _
        pe.category = EVENT_CATEGORIES[i%len(EVENT_CATEGORIES)][0]
        pe.registrable_online = i%2
        pe.begin_registration = i%2
        pe.team_event = i%2
        if pe.team_event:
            pe.team_size_max = i%10
        pe.has_tdp = i%2
        pe.has_questionnaire = i%2
        pe.save()

    #Audience Events
    print "Creating", AUDIENCE_EVENT_RANGE,"Audience Events"
    for i in range(AUDIENCE_EVENT_RANGE):
        if AudienceEvent.objects.filter(title="_AEvent" + str(i)).count():
            continue
        ae = AudienceEvent()
        ae.title = "_AEvent" + str(i)
        ae.category = EVENT_CATEGORIES[i%len(EVENT_CATEGORIES)][0]
        ae.save()

    #Tabs for events
    print "Creating", TAB_RANGE,"Tabs for each event"
    for e in GenericEvent.objects.filter(title__startswith='_'):#and here it is :P
        for i in range(TAB_RANGE):
            if Tab.objects.filter(title="Tab" + str(i)).count():
                continue
            tb = Tab()
            tb.title = "Tab" + str(i)
            tb.text = "This is Tab" + str(i)
            tb.pref = i%10
            tb.event = e
            tb.save()


 
