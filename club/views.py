from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .models import Club, Club_Admin, Club_User
from home.models import Wanted_Beers, Beer_Banner
from django.utils import timezone
from django.utils.timezone import datetime

# Create your views here.
context = {}

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
		context['clubs'] = clubs
    return render(request, 'club/index.html', context)  
	
def club(request, id):
    user_object = request.user
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    context['user_object'] = user_object
    return render(request, 'club/club.html', context)  