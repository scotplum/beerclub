from club.models import Club, Club_User
from django.contrib.auth.models import User
from home.models import Beer_Banner
from home.forms import findbeerForm

def navigation(request):
	#Build the context for this user, check Beer Banner and assign Club links for navigation
    context = {}
    user_object = request.user
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    context['user_object'] = user_object
    club_check = Club_User.objects.filter(user=user_object).exists()
    context['club_check'] = club_check    
    if club_check:
		context['clubs'] = Club_User.objects.filter(user=user_object.id).filter(is_active=True).select_related()
    return {'context':context, 'user_object':user_object, 'club_check':club_check}