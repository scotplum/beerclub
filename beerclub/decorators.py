from club.models import Club_User, Club
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