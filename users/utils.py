from events.models import ParticipantEvent
from mainsite_2014.settings import DATABASES
erp_db = DATABASES.keys()[1]
from django.utils import timezone


#This is a utility function, can be called from anywhere
#returns all events that at a time can be registered
def registrable_events(time=timezone.now(),user = None):
    #TODO:change erp
    if user is None:
        return None
    eventlist = []
    for event in ParticipantEvent.objects.using(erp_db).filter(registrable_online=True).filter(registration_ends > time).filter(registration_starts<time):
        if event not in user.get_profile().get_regd_events():
            eventlist.append(event.title)
    return eventlist


