from users.models import UserProfile, College
from django.contrib.auth.models import User
from events.models import ParticipantEvent
from dashboard.models import TeamEvent
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseForbidden, HttpResponse
from django.conf import settings
erp_db = settings.DATABASES.keys()[1]


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase.pdfmetrics import getFont, getAscentDescent
from reportlab.platypus import Paragraph, Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
    
import datetime

def PDFSetFont(pdf, font_name, font_size):
    """
    Sets the font and returns the lineheight.
    """

    pdf.setFont(font_name, font_size)
    (ascent, descent) = getAscentDescent(font_name, font_size)
    return ascent - descent  # Returns line height

def paintParagraph(pdf, x, y, text):

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name = 'paraStyle', fontSize = 12))
    
    p = Paragraph(text, styles['paraStyle'], None) # None for bullet type

    (A4Width, A4Height) = A4
    availableWidth = A4Width - 2 * cm  # Leaving margins of 1 cm on both sides
    availableHeight = y
    (paraWidth, paraHeight) = p.wrap(availableWidth, availableHeight)  # find required space
    
    p.drawOn(pdf, x, y - paraHeight)
    
    y -= paraHeight + cm
    
    return y

def paintImage(pdf, x, y, im):

    (A4Width, A4Height) = A4
    availableWidth = A4Width - 2 * cm  # Leaving margins of 1 cm on both sides
    availableHeight = y
    (imWidth, imHeight) = im.wrap(availableWidth, availableHeight)  # find required space
    
    im.drawOn(pdf, x, y - imHeight)
    
    x -= imWidth + cm
    y -= imHeight + cm
    
    return (x, y)

############Change: /home/shaastra to change for local
def initNewPDFPage(pdf, (pageWidth, pageHeight), shaastra_id, username):
    """
    Paints the headers on every new page of the PDF document.
    Also returns the coordinates (x, y) where the last painting operation happened.
    """

    y = pageHeight

    # Leave a margin of one cm at the top

    y = pageHeight - cm
    x = cm

    im = Image("/home/shaastra/hospi/participantPDFs_2k14/shaastralogo.jpg", width=3*inch, height=1.8*inch)
    im.hAlign = 'LEFT'
    
    (x, t) = paintImage(pdf, x, y, im)

    # Set font for Header
    lineheight = PDFSetFont(pdf, 'Times-Bold', 20)

    # Page number in same line, right aligned
    
    y = pageHeight-2*cm

    pdf.drawRightString(pageWidth - cm*1.5, y, '%s' % shaastra_id)

    y -= lineheight + cm
    
    lineheight = PDFSetFont(pdf, 'Times-Roman', 18)
    
    pdf.drawRightString(pageWidth - cm*1.5, y, '%s' % username)

    return t
    
def printParticipantDetails(pdf, x, y, user, userProfile):

    #accountDetails =  'Username:     <b>' + user.username + '</b> (UID: ' + str(user.id) + ')<br/><br/>'
    #accountDetails += 'Shaastra ID:  <b>%s</b><br/><br/>' % userProfile.shaastra_id
    accountDetails = ''
    if user.first_name and user.last_name:
        accountDetails +=  'Name:         <b>%s %s</b><br/><br/>' % (user.first_name, user.last_name)
    else:
        accountDetails +=  'Name:         <br/><br/>'
    accountDetails += 'Email:        <b>%s</b><br/><br/>' % user.email if user.email else ''
    ##########Added shaastra ID to printParticipantDetails
    accountDetails += 'Shaastra ID:  <b>%s</b><br/><br/>' % userProfile.shaastra_id
    
    accountDetails += 'Mobile No:    <b>%s</b><br/><br/>' % userProfile.mobile_number if userProfile.mobile_number else ''
    try:
        accountDetails += 'College:      <b>%s</b><br/><br/>' % userProfile.college.name
    except:
        accountDetails += 'College:      <b>%s</b><br/><br/>' % ''
    #accountDetails += 'College Roll: <b>%s</b><br/><br/>' % userProfile.college_roll
    try:
        accountDetails += 'City:         <b>%s</b><br/><br/>' % userProfile.college.city
    except:
        accountDetails += 'City:         <b>%s</b><br/><br/>' % ''
    try:
        accountDetails += 'State:        <b>%s</b><br/><br/>' % userProfile.college.state
    except:
        accountDetails += 'State:        <b>%s</b><br/><br/>' % ''
    accountDetails += 'Branch:       <b>%s</b><br/><br/>' % userProfile.branch if userProfile.branch else ''
    if userProfile.gender == 'M':
        accountDetails += 'Gender:       <b>%s</b><br/><br/>' % 'Male'
    elif userProfile.gender == 'F':
        accountDetails += 'Gender:       <b>%s</b><br/><br/>' % 'Female'
    else:
        accountDetails += 'Gender:       <b>%s</b><br/><br/>' % ''
    accountDetails += 'Age:          <b>%s</b><br/><br/>' % str(userProfile.age) if userProfile.age else ''

    #if userProfile.want_accomodation:
    #    accountDetails += '<br/><b>Accomodation requested</b><br/><br/>'
    #else:
    #    accountDetails += '<br/><b>Accomodation not requested</b><br/><br/>'
    
    y = paintParagraph(pdf, x, y, accountDetails)

    accountInstruction = 'Attention: <b>If you have not created an account on the Shaastra website</b>, an account has been created for you. Both your username and password are the local part of your email address. E.g. if your email is \'example@domain.com\', both your username and password will be \'example\' (without the quotes). <b>Please do update your profile on the Shaastra website to avoid any inconvenience later.</b>'
    
    y = paintParagraph(pdf, x, y, accountInstruction)
    
    qmsInstruction = '<para alignment="center"><font size=14><b>Instructions</b></font>'
    
    y -= cm*0.7
    y = paintParagraph(pdf, x, y, qmsInstruction)
    #--------------------------
    qmsInstruction = '</para><para alignment="left"><br/><br/><b>1.  Please bring a printed copy of this file while coming to Shaastra.</b><br/><br/>2.Present this print out to the Registration Desk situated at KV Grounds in IIT Madras along with your College ID for verification. If you have already been confirmed accomodation or selected for a pre-registered event, you may proceed to the Hospitality Control Rooms (Godavari for Boys, Sharavati for girls).  <br/><br/>3. Upon paying a registration fee of Rs 150, you would receive your unique Shaastra Passport.<br/><br/>4. This Passport is necessary in order to participate in any event or workshop/ attend any lecture or show at Shaastra.  <br/><br/>5.  For more information, please drop us a mail at outreach@shaastra.org<br/><br/>QMS Team</para>'
    #!!!!!! qms@shaastra.org
    y += cm*0.7
    y = paintParagraph(pdf, x, y, qmsInstruction)

    return y
    
def printEventParticipationDetails(pdf, x, y, user, singularEventRegistrations, userTeams):

    lineheight = PDFSetFont(pdf, 'Times-Bold', 16)

    (A4Width, A4Height) = A4

    pdf.drawCentredString(A4Width/2, y, 'PARTICIPATION DETAILS')

    y -= lineheight + cm

    # Construct the table data
    
    sNo = 1
    #!!!!!!!
    tableData = [ ['Serial No', 'Event Name', 'Team Name', 'Team ID'] ]
    #!!!!!!
    """
    for eventRegistration in singularEventRegistrations:
        tableData.append([sNo, eventRegistration.event.title, '', ''])
        sNo += 1
    """  
    for team in userTeams:
        teamname_str = 'Not provided during regn.'
        if team.team_name:
            teamname_str = team.team_name
        tableData.append([sNo, team.get_event().title, teamname_str, team.team_id])
        sNo += 1
        
    t = Table(tableData, repeatRows=1)

    # Set the table style

    tableStyle = TableStyle([ ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'), # Font style for Table Data
                              ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'), # Font style for Table Header
                              ('FONTSIZE', (0, 0), (-1, -1), 12),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTRE'),
                              ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ])
    t.setStyle(tableStyle)
    (A4Width, A4Height) = A4
    availableWidth = A4Width - 2 * cm  # Leaving margins of 1 cm on both sides
    availableHeight = y
    (tableWidth, tableHeight) = t.wrap(availableWidth, availableHeight)  # find required space
    
    t.drawOn(pdf, x, y - tableHeight)
    
def generateParticipantPDF(user):

    userProfile = UserProfile.objects.get(user = user)
    
    # Create a buffer to store the contents of the PDF.
    # http://stackoverflow.com/questions/4378713/django-reportlab-pdf-generation-attached-to-an-email
    buffer = StringIO()

    # Create the PDF object, using the response object as its "file."

    pdf = canvas.Canvas(buffer, pagesize=A4)

    # Define the title of the document as printed in the document header.

    page_title = 'PARTICIPANT DETAILS'

    # Get the width and height of the page.

    (A4Width, A4Height) = A4

    # Paint the headers and get the coordinates 

    y = initNewPDFPage(pdf, A4, userProfile.shaastra_id, userProfile.user.username)

    # Setting x to be a cm from the left edge

    x = cm

    # Print Participant Details in PDF

    y = printParticipantDetails(pdf, x, y, user, userProfile)
    
    # Print Event Participation Details in PDF
    
    #singularEventRegistrations = EventSingularRegistration.objects.filter(user = user)
    #!!!!!!!!!!!!
    """
    try:
        teamevents = user.get_profile().get_regd_events()
    except:
        teamevents = []
    #userTeams = user.joined_teams.all()
    #!!!!!!!!
    #if (not singularEventRegistrations) and (not userTeams):
        # The user is not registered for any event.
    if not teamevents:
        buffer.close()
        #return None
        y -= cm * 0.5
        pdf.drawString(x, y, 'You are not registered for any events this Shaastra')
    
    else:
        pdf.showPage()
        y = initNewPDFPage(pdf, A4, userProfile.shaastra_id, userProfile.user.username)
        
        printEventParticipationDetails(pdf, x, y, user, None, teamevents)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!Y COMMENTED@@@@@@@@@@@@
    """
    pdf.showPage()
    pdf.save()

    response = buffer.getvalue()
    buffer.close()

    return response
    
###########/home/shaastra
def log(msg):
    #!!!!!!!!!!!!!!!!!!!!!!!
    destination = open('/home/shaastra/hospi/participantPDFs_2k14/log2.txt', 'a')
    destination.write(str(msg))
    destination.write('\n')
    destination.close()
    print msg
#########Confirm if Dear Participant only or name
##########CHange entire content!!!!!!!!!!!!!
def mailPDF(user, pdf):
    return
    subject = '[IMPORTANT] Registration Details, Shaastra 2014'
    message = 'Dear '
    if user.first_name and user.last_name:
        message += user.first_name.title() + ' ' + user.last_name.title()
    elif user.first_name:
        message += user.first_name.title()
    elif user.last_name:
        message += user.last_name.title()
    elif user.username:
        message += user.username
    else:
        message += 'Participant'
    message +=','
    file_msg = open('message.txt','r')
    message += file_msg.read()
    file_msg.close()
    email = user.email
    #!!!!!change qm@shaastra.org to outreach@shaastra.org??????////
    #!!!!!!!!!!!!!!!!
    #email = 'swopstesting@gmail.com' #TODO: Remove this line for finale
    #######################################*****************************
    msg = EmailMultiAlternatives(subject, message, 'noreply@shaastra.org' , [email,])
    #msg = EmailMultiAlternatives(subject, message, 'gowtham.vg.7@gmail.com' , [email,])
    msg.content_subtype = "html"
    try:
        userprofile = user.get_profile()
    except:
        log(user.username + "failed to mail as userProfile does not exist\n")
        return
    try:
        msg.attach('%s-registration-details.pdf' % user.get_profile().shaastra_id, pdf, 'application/pdf')
    except:
        log("%s: attachment failed" % userprofile.shaastra_id)
        return
    ##########
    msg.send()
    log('Mail sent to %s' % email) 
#######change /home/shaastra for pdf location
def savePDF(pdf, user):
    #!!!!!!!
    try:
        destination = open('/home/shaastra/hospi/participantPDFs_2k14/'+user.get_profile().shaastra_id+'-registration-details.pdf', 'wb+')
    except:
        log(user.username + "userprofile does not exist")
        return
    destination.write(pdf)
    destination.close()
    log('File '+user.get_profile().shaastra_id+'-registration-details.pdf saved.')
########calls mailPDF!!!!!!!!
def generatePDFs(uid):
    
    #participants = []
    #numPDFsGenerated = 0
    #numPDFsMailed = 0
    #userProfilesWithShaastraIds = UserProfile.objects.exclude(shaastra_id = '') #TODO Exclude non active users??
    #participantProfilesWithShaastraIds = userProfilesWithShaastraIds.exclude(is_core = True).filter(user__is_superuser = False)
    #for profile in participantProfilesWithShaastraIds:
    #    try:
    #        u = profile.user
    #    except:
    #        continue
    #    participants.append(u)
    #!!!!!!!!!!!!!!finale???
    participants = [User.objects.get(id = uid)] #TODO: Remove this line for finale

    for participant in participants:
        #if participant.id < 7071:
        #    continue
        log(participant.id)
        pdf = generateParticipantPDF(participant)
        if pdf is None:
            continue
        savePDF(pdf, participant)
        """
        if participant.email:
            mailPDF(participant, pdf)
        """
    #        numPDFsMailed += 1
        
    #    numPDFsGenerated += 1
    #log('\n\nPDFs generated: %d' % numPDFsGenerated)
    #log('\n\nPDFs mailed: %d' % numPDFsMailed)
    
def remainingPDFs():
    #!!!!!!!!!!!!!!!
    return ('Comment this line to send the Participant PDFs.')
    
    log('\n\n**********  Now: %s  **********' % datetime.datetime.now())

    fileNameList = ['/home/shaastra/hospi/participantPDFs_2k14/ssq.txt', '/home/shaastra/hospi/participantPDFs_2k14/rws.txt']
    
    for fileName in fileNameList:

        participants = []
        emails = []

        fileObj = open(fileName, 'r')
        log('\n\nOpened %s.' % fileName)
        for line in fileObj:
            t = line[:-1]  # -1 to remove the last \n character.
            if t:
                emails.append(t)
        fileObj.close()
        log('Closed %s.' % fileName)

        emails = list(set(emails))  # To get rid of duplicates
        #!!!!!!!!participants is [] always!!!!!!!!!!
        for email in emails:
            usersMatchingEmail = User.objects.filter(email = email)
            if len(usersMatchingEmail) == 1:
                participants.append(usersMatchingEmail[0])
            elif len(usersMatchingEmail) < 1:
                log('No users matching %s' % email)
            else:
                log('More than one users matching %s' % email)

        for participant in participants:
            log(participant.id)
            pdf = generateParticipantPDF(participant)
            if pdf is None:
                continue
            savePDF(pdf, participant)
            if participant.email:
                mailPDF(participant, pdf)
                #break  #TODO: Remove this for the finale
##########/home/shaastra mailed.txt  local
def mailRoundTwo():
    
    log('\n\n**********  Now: %s  **********' % datetime.datetime.now())

    uids = []
    
    participants = []
    #!!!TODO??
    userProfilesWithShaastraIds = UserProfile.objects.exclude(shaastra_id = '') #TODO Exclude non active users??
    participantProfilesWithShaastraIds = userProfilesWithShaastraIds.exclude(is_core = True).filter(user__is_superuser = False)
    for profile in participantProfilesWithShaastraIds:
        try:
            u = profile.user
        except:
            continue
        participants.append(u)

    fileObj = open('/home/shaastra/hospi/participantPDFs_2k14/mailed.txt', 'r')
    log('\n\nOpened %s to get uids of all mailed participants.' % 'mailed.txt')
    for line in fileObj:
        t = line[:-1]  # -1 to remove the last \n character.
        if t:
            uids.append(t)
    fileObj.close()
    log('Closed %s.' % 'mailed.txt')
    
    uids = list(set(uids))  # To get rid of duplicates
    log('Found: %d uids have been mailed already.' % len(uids))
    
    for uid in uids:
        try:
            participants.remove(User.objects.get(pk=int(uid)))
        except User.DoesNotExist:
            continue
        except ValueError:
            continue
        else:
            log('Already mailed uid %d. Removing from mailing list.' % int(uid))
        
    for participant in participants:
        log(participant.id)
        pdf = generateParticipantPDF(participant)
        if pdf is None:
            continue
        savePDF(pdf, participant)
        if participant.email:
            mailPDF(participant, pdf)
            #break  #TODO: Remove this for the finale
            
def checkData(**kwargs):

    for key in kwargs.keys():
        if key[:len('UserProfile')] == 'UserProfile':
            finalKey = key[len('UserProfile'):]
            searchParams = {finalKey: kwargs[key]}
            profiles = UserProfile.objects.filter(**searchParams)
            users = []
            for profile in profiles:
                try:
                    users.append(profile.user)
                except:
                    continue
        else:
            finalKey = key
            searchParams = {finalKey: kwargs[key]}
            users = User.objects.filter(**searchParams)
        if len(users) == 0:
            print 'No users found with the input data'
            return None
        else:
            print 'Data found...\n'
            for user in users:
                string = user.username + ': ' + user.first_name + ' ' + user.last_name + ' (' + str(user.id) + ')  -->  '
                string += user.email
                #singularEventRegistrations = EventSingularRegistration.objects.filter(user = user)
                
                #userTeams = user.joined_teams.all()
                #!!!!!!
                try:
                    userTeams = user.get_profile().get_regd_events()
                except:
                    userTeams = None
                #string += '\n  Singular Events:' + str(singularEventRegistrations)
                repeat_userTeams = clean_Teams(teams = userTeams,profile = user.get_profile())
                userTeams = [userTeam for userTeam in userTeams if userTeam not in repeat_userTeams]
                for userTeam in userTeams:
                    string += '\n  Teams:' + str(userTeam)
                string += '\n'
                for userTeam in repeat_userTeams:
                    string += '\n  Teams:' + str(userTeam)
                string += '\n    '
                try:
                    #!!!!
                    f = open('/home/shaastra/hospi/participantPDFs_2k14/SHA'+str(1400000+user.pk)+'-registration-details.pdf', 'r')
                except:
                    
                    if not userTeams:
                        string += 'NO mail required'
                    else:
                        string += 'NOT mailed'                    
                    pass
                else:
                    f.close()
                    string += 'Mailed\n'
                print string

            if len(users) == 1:
                return users[0]
                
            else:
                return users
#!!! has only return
def clean_Teams(teams,profile):
    cteam = []
    event_id_list = [team.event_id for team in teams]
    if list(set(event_id_list))!= event_id_list:
        repeat_event_ids = list(set( [x for x in event_id_list if event_id_list.count(x) > 1]))
        return [tev for tev in TeamEvent.objects.filter(users__username=profile.user.username) if tev.event_id in repeat_event_ids]

        
    return None
        

def addLeadersToMembers():
    return
    teams = Team.objects.all()
    for team in teams:
        print team.name
        try:
            l = team.leader
        except:
            print 'Bad team. No leader.'
            print '\n'
            continue
        if l not in team.members.all():
            print 'Leader: ' + l.username
            print str(team.members.all())
            team.members.add(l)
            print 'After adding: ' + str(team.members.all())
            print '\n'
          
def createUser(fullname=None, email=None, mobile=None, college=None):

    try:
        newUser = User.objects.get(username = email.split('@')[0])
    except User.DoesNotExist:
        newUser = User()
        newUser.email = email
        newUser.username = email.split('@')[0]
        newUser.first_name = fullname
        newUser.set_password('default')
        newUser.is_active = True
        newUser.save()
        # Get the college
        try:
            newCollege = College.objects.get(name = college)
        except:
            newCollege = College.objects.get_or_create(name = 'Default', city = 'Default', state = 'Default')
        # Create the user's profile
        newUserProfile = UserProfile()
        newUserProfile.user = newUser
        newUserProfile.mobile_number = mobile
        newUserProfile.gender = 'F'
        newUserProfile.age = 0
        newUserProfile.shaastra_id = 'SHA' + str(1400000 + newUser.id)
        newUserProfile.college = newCollege
        newUserProfile.branch = 'Others'
        newUserProfile.want_accomodation = False
        newUserProfile.save()
    return newUser
            
def checkParticipationDetailsCSV(path, event_name):
    try:
        partFile = open(path, 'r')
    except IOError:
        print 'Could not open %s.' % path
        return
    print 'Read file opened.'
    try:
        outFile = open(path[:-4]+'_out.csv', 'w')
    except IOError:
        print 'Could not open write file %s.' % (path[:-3]+'out.csv')
        return
    print 'Out file opened.'
    try:
        e = ParticipantEvent.objects.using(erp_db).filter(title = event_name)[0]
    except ParticipantEvent.DoesNotExist:
        print 'Event \'%s\' not found.' % event_name
        return
    print 'Event obtained.\n'

    for line in partFile:
        print 'Line read: %s' % line
        line = line[:-1]  # -1 to remove the last \n character.
        outLine = line
        data = line.split(',')
        if not data[0].isdigit():  # The first column in the CSV should be a serial number
            print 'First entry not S.No. Continuing...\n'
            continue
        u = User.objects.filter(email=data[3])
        if not u:
            # User not found
            print 'Email not found. Trying to create...'
            u = [createUser(college=data[1], fullname=data[2], email=data[3], mobile=data[4])]
            outLine += ', user Created'
        else:
            # User found
            print 'User found.'
            outLine += ', user Found'
        if len(u) == 1:
            # one user found
            # check registration for event
            # if not registered, register
            u = u[0]
            #!!!!!!!!!!!!!!!!!!!TODO:?????????????///
            try:
                regn = u.get_profile().get_regd_events()
            except:
                regn = []
            regn2 = []
            for r in regn:
                if r.event_id == e.id:
                    regn2.append(r)
            regn = regn2
            #regn = EventSingularRegistration.objects.filter(user = u).filter(event = e)
            if not regn:
                # The user is not registered
                # go ahead and register
                regn = TeamEvent(event_id = e.id)
                regn.save()
                regn.users.add(u)
                #regn.event = e
                regn.save()
                outLine += ', new regn'
                
            elif len(regn) == 1:
                #!!!!!!!!!!!WHERE IS regn used???????????////
                # User is registered
                # Check if mailed
                try:
                    temp = open('/home/shaastra/hospi/participantPDFs_2k14/SHA'+str(1400000+u.pk)+'-registration-details.pdf', 'r')
                except IOError:
                    # PDF not found.
                    # Not mailed.
                    outLine += ', not mailed'
                else:
                    # PDF found
                    # mailed
                    #!!!!!!!MAILED???
                    outLine += ', Mailed'
                    temp.close()
                
            else:
                # More than one registrations found.
                # Write this to file
                outLine += ', >1 regn found'
            
        else:
            # More than one user found.
            # write this to file
            outLine += ', >1 user found,'
        outLine += '\n'
        outFile.write(outLine)
        
    partFile.close()
    outFile.close()
##############################WTH is the function below!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
def cleanParticipationCSV(path):
    f = open(path, 'r')
    t = open(path[:-4]+'_mod.csv', 'w')
    for l in f:
        q = False
        n = ''
        for i in range(len(l)):
            if l[i] == '\"':
                if q is True: q = False
                else: q = True
            if l[i] == ',' and q is True: n += ''
            elif l[i] == '\"': n += ''
            else: n += l[i]
        t.write(n)
    f.close()
    t.close()

########Ok...but y will it have ,...n y is it being deleted?? 
def cleanEmails():
    for u in User.objects.all():
        if u.email and u.email[-1] == ',':
            print u.id
            print u.email
            u.email = u.email[:-1]
            print u.email
            try:
                os.remove('/home/shaastra/hospi/participantPDFs_2k14/SHA'+str(1400000+u.id)+'-registration-details.pdf')
            except OSError:
                print 'PDF doesn\'t exist.'
            else:
                print 'PDF deleted.'
            u.save()
            print '\n'
