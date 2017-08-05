from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .models import Club, Club_Admin, Club_User, Club_Announcement, Club_Event
from home.models import Wanted_Beers, Beer_Banner
from django.utils import timezone
from django.utils.timezone import datetime

# Create your views here.
context = {}

@login_required
def index(request):
    user_object = request.user
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    context['user_object'] = user_object
    club_check = Club_User.objects.filter(user=user_object).exists()
    context['club_check'] = club_check
    if club_check:
		clubs = Club_User.objects.filter(user=user_object)
		club_count = len(Club_User.objects.filter(user=user_object))
		context['club_count'] = club_count
		context['clubs'] = clubs
		if club_count == 1:
			club = Club_User.objects.get(user=user_object) 
			club_id = club.id
			return redirect('/club/' + str(club_id) + '/')
    return render(request, 'club/index.html', context)  

@login_required	
def club(request, id):
    user_object = request.user
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    context['user_object'] = user_object
    crowd = Club.objects.get(id=id)
    crowd_announcement_check = Club_Announcement.objects.filter(club=crowd).exists()
    club_event_check = Club_Event.objects.filter(club=crowd).exists()
    club_user_check = Club_User.objects.filter(club=crowd).exists()
    context['crowd_announcement_check'] = crowd_announcement_check
    context['club_event_check'] = club_event_check
    context['club_user_check'] = club_user_check
    if crowd_announcement_check:
		crowd_announcement = Club_Announcement.objects.filter(club=crowd)
		context['crowd_announcement'] = crowd_announcement
    if club_event_check:
		club_event = Club_Event.objects.filter(club=crowd)
		context['club_event'] = club_event
    if club_user_check:
		club_user = Club_User.objects.filter(club=crowd)
		context['club_user'] = club_user
    context['crowd'] = crowd
    return render(request, 'club/club.html', context)  