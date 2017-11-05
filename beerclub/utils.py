from club.models import Club, Club_User
from django.contrib.auth.models import User
from home.models import Beer_Banner
from home.forms import findbeerForm
import re

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
    #Check to see if user is on a mobile device or not and save to session
    if 'is_mobile' not in request.session:
		MOBILE_AGENT_RE=re.compile(r".*(iphone|android)", re.IGNORECASE)		
		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			request.session['is_mobile'] = True
		else:
			request.session['is_mobile'] = False
    return {'context':context, 'user_object':user_object, 'club_check':club_check}
	
	
def mobile(request):
	MOBILE_AGENT_RE=re.compile(r".*(iphone|android)", re.IGNORECASE)
	
	if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
		return True
	else:
		return False