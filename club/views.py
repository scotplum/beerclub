from __future__ import division
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .models import Club, Club_Admin, Club_User, Club_Announcement, Club_Event
from home.models import Wanted_Beers, Beer_Banner, Beer_Rating
from star_ratings.models import UserRating, Rating
from django.utils import timezone
from django.utils.timezone import datetime
from operator import itemgetter
from beerclub.decorators import user_is_admin

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
			club_id = club.club.id
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
    club_admin = Club_Admin.objects.filter(club=crowd)
    crowd_announcement_check = Club_Announcement.objects.filter(club=crowd).exists()
    club_event_check = Club_Event.objects.filter(club=crowd).exists()
    club_user_check = Club_User.objects.filter(club=crowd).exists()
    club_admin_check = Club_Admin.objects.filter(club=crowd).filter(user=user_object).exists()
    beer_rating_check = UserRating.objects.filter(user=user_object).exists()
    context['club_admin'] = club_admin
    context['club_admin_check'] = club_admin_check
    context['beer_rating_check'] = beer_rating_check
    context['crowd_announcement_check'] = crowd_announcement_check
    context['club_event_check'] = club_event_check
    context['club_user_check'] = club_user_check
    context['crowd'] = crowd
    if crowd_announcement_check:
		crowd_announcement = Club_Announcement.objects.filter(club=crowd)
		context['crowd_announcement'] = crowd_announcement
    if club_event_check:
		club_event = Club_Event.objects.filter(club=crowd)
		context['club_event'] = club_event
    user_beer_rating = []    
    if club_user_check:
		club_user = Club_User.objects.filter(club=crowd)
		context['club_user'] = club_user
#    return render(request, 'club/club.html', context)  
		for u in club_user:
			if u.is_active:
				rating_user_check = UserRating.objects.filter(user=u.user.id).exists()
				if rating_user_check:
					beer_rating = UserRating.objects.filter(user=u.user.id)
					for beer in beer_rating:
						rated_beer = Beer_Rating.objects.get(bdb_id = beer.rating.content_object.bdb_id)
						user_beer_rating.append(rated_beer)
				user_beers = list(set(user_beer_rating))
				context['user_beers'] = user_beers
    club_beer = []
    club_beer_sorted = []
    for b in user_beers:
		b_rating = Rating.objects.filter(Beer_Rating=b)
		b_score = 0
		b_count = 0
		b_list = []
		b_dict = {}
		b_user = []
		for c_u in club_user:
			if c_u.is_active:
				if UserRating.objects.filter(rating=b_rating).filter(user=c_u.user).exists():
					b_count += 1
					b_userrating = UserRating.objects.filter(rating=b_rating).filter(user=c_u.user)
					for s in b_userrating:
						b_score = b_score + s.score
						b_user.append(c_u.user)
		b_dict['username'] = b_user
		b_dict['name'] = b
		b_dict['score'] = b_score
		b_dict['count'] = b_count
		b_dict['avg'] = b_score / b_count
		club_beer.append(b_dict)
    club_beer_sorted = sorted(club_beer, key=itemgetter('avg'), reverse=True)[:10]
    context['club_beer_sorted'] = club_beer_sorted
    return render(request, 'club/club.html', context) 
	
@login_required
@user_is_admin
def manage(request, id):
    user_object = request.user
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    context['user_object'] = user_object
    club_check = Club_User.objects.filter(user=user_object).exists()
    context['club_check'] = club_check
    crowd = Club.objects.get(id=id)
    context['crowd'] = crowd
    club_admin_check = Club_Admin.objects.filter(club=crowd).filter(user=user_object).exists()
    context['club_admin_check'] = club_admin_check
    return render(request, 'club/manage.html', context)  

@login_required
@user_is_admin	
def announcement(request, id):
    user_object = request.user
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    context['user_object'] = user_object
    club_check = Club_User.objects.filter(user=user_object).exists()
    context['club_check'] = club_check
    crowd = Club.objects.get(id=id)
    context['crowd'] = crowd
    club_admin_check = Club_Admin.objects.filter(club=crowd).filter(user=user_object).exists()
    context['club_admin_check'] = club_admin_check
    return render(request, 'club/announcement.html', context)  

@login_required
@user_is_admin	
def about(request, id):
    user_object = request.user
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    context['user_object'] = user_object
    club_check = Club_User.objects.filter(user=user_object).exists()
    context['club_check'] = club_check
    crowd = Club.objects.get(id=id)
    context['crowd'] = crowd
    club_admin_check = Club_Admin.objects.filter(club=crowd).filter(user=user_object).exists()
    context['club_admin_check'] = club_admin_check
    return render(request, 'club/about.html', context)  

@login_required
@user_is_admin	
def membership(request, id):
    user_object = request.user
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    context['user_object'] = user_object
    club_check = Club_User.objects.filter(user=user_object).exists()
    context['club_check'] = club_check
    crowd = Club.objects.get(id=id)
    context['crowd'] = crowd
    club_admin_check = Club_Admin.objects.filter(club=crowd).filter(user=user_object).exists()
    context['club_admin_check'] = club_admin_check
    return render(request, 'club/membership.html', context)  

@login_required
@user_is_admin	
def event(request, id):
    user_object = request.user
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    context['user_object'] = user_object
    club_check = Club_User.objects.filter(user=user_object).exists()
    context['club_check'] = club_check
    crowd = Club.objects.get(id=id)
    context['crowd'] = crowd
    club_admin_check = Club_Admin.objects.filter(club=crowd).filter(user=user_object).exists()
    context['club_admin_check'] = club_admin_check
    return render(request, 'club/event.html', context)  