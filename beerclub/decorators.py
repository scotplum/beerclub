from club.models import Club_User, Club, Club_Event
from home.models import Beer_Note, Brewery_Note
from event.models import Event
from django.core.exceptions import PermissionDenied

def user_is_admin(function):
    def wrap(request, *args, **kwargs):
        user_object = request.user
        crowd = Club.objects.get(id=kwargs['id'])
        admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()		
        if admin_check:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
	
def event_is_active(function):
    def wrap(request, *args, **kwargs):
        event = Event.objects.get(id=kwargs['event_id'])
        if event.is_active:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
	
def user_is_member(function):
    def wrap(request, *args, **kwargs):
        user_object = request.user
        event = Event.objects.get(id=kwargs['event_id'])
        club_event = Club_Event.objects.get(event=event)
        crowd = Club.objects.get(id=club_event.club_id)
        member_check = Club_User.objects.filter(club=crowd).filter(user=user_object).exists()		
        if member_check:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def beernote_is_user(function):
    def wrap(request, *args, **kwargs):
        user_object = request.user
        note = Beer_Note.objects.get(id=kwargs['id'])		
        if user_object == note.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
	
def brewerynote_is_user(function):
    def wrap(request, *args, **kwargs):
        user_object = request.user
        note = Brewery_Note.objects.get(id=kwargs['id'])		
        if user_object == note.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap