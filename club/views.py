from __future__ import division
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .models import Club, Club_User, Club_Announcement, Club_Event, Club_Application
from event.models import Event, Event_Address
from forms import ClubForm, ClubAnnouncementForm
from event.forms import EventForm, EventAddressForm, EventEditForm, EventAddressEditForm
from django.forms import modelformset_factory
from home.models import Wanted_Beers, Beer_Banner, Beer_Rating
from star_ratings.models import UserRating, Rating
from django.utils import timezone
import datetime
from operator import itemgetter
from beerclub.decorators import user_is_admin
from beerclub.utils import navigation

# Create your views here.
context = {}

@login_required
def index(request):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    return render(request, 'club/index.html', context)  

@login_required	
def club(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    club_beer = []
    club_admin = Club_User.objects.filter(club=crowd).filter(is_admin=True).select_related('user','club')
    crowd_announcement_check = Club_Announcement.objects.filter(club=crowd).exists()
    club_event_check = Club_Event.objects.filter(club=crowd).exists()
    club_user_check = Club_User.objects.filter(club=crowd).exists()
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    club_db_user_check = Club_User.objects.filter(club=crowd).filter(user=user_object).exists()
    club_application_pending_check = Club_Application.objects.filter(club=crowd).filter(user=user_object).filter(status='pending').exists()
    club_admin_pending_check = Club_Application.objects.filter(club=crowd).filter(status='pending').exists()
    beer_rating_check = UserRating.objects.filter(user=user_object).exists()
    context['club_admin'] = club_admin
    context['club_admin_check'] = club_admin_check
    context['beer_rating_check'] = beer_rating_check
    context['crowd_announcement_check'] = crowd_announcement_check
    context['club_event_check'] = club_event_check
    context['club_user_check'] = club_user_check
    context['crowd'] = crowd
    context['club_db_user_check'] = club_db_user_check
    context['club_application_pending_check'] = club_application_pending_check
    context['club_admin_pending_check'] = club_admin_pending_check
    if crowd_announcement_check:
		crowd_announcement = Club_Announcement.objects.filter(club=crowd).select_related('club')
		context['crowd_announcement'] = crowd_announcement
    if club_event_check:
		club_event = Club_Event.objects.filter(club=crowd).select_related('club', 'event')
		context['club_event'] = club_event
    user_beer_rating = []    
    if club_user_check:
		club_user = Club_User.objects.filter(club=crowd).filter(is_active=True).select_related('user','club')
		context['club_user'] = club_user
		user_beer_rating = []
		club_beer = []
		club_beer_sorted = []
		for u in club_user:
			rating_user_check = UserRating.objects.filter(user=u.user.id).exists()
			if rating_user_check:
				beer_rating = UserRating.objects.filter(user=u.user.id).select_related('user', 'rating')
				user_beer_rating.append(beer_rating)
				context['beer_rating'] = user_beer_rating
			for b in user_beer_rating:
				for set in b:
					club_beer.append(set)
			context['club_beer'] = club_beer
    if request.method == "POST": 
		rp = request.POST
		if 'apply' in rp:
			club_member = Club_Application(user=user_object, club=crowd)
			club_member.save()
			return redirect('/club/' + id + '/')
    return render(request, 'club/club.html', context) 
	
@login_required
@user_is_admin
def manage(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    context['crowd'] = crowd
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    return render(request, 'club/manage.html', context)  

@login_required
@user_is_admin	
def announcement(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    context['crowd'] = crowd
    crowd_announcement_check = Club_Announcement.objects.filter(club=crowd).exists()
    context['crowd_announcement_check'] = crowd_announcement_check
    if crowd_announcement_check:
		crowd_announcement = Club_Announcement.objects.filter(club=crowd)
		context['crowd_announcement'] = crowd_announcement
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    context['form'] = ClubAnnouncementForm(instance=crowd)
    ClubAnnouncementFormSet = modelformset_factory(Club_Announcement, exclude=('expiration_date','club',))
    formset = ClubAnnouncementFormSet(queryset=Club_Announcement.objects.filter(club=crowd))
    context['formset'] = formset
    if request.method == 'POST':
        formset = ClubAnnouncementFormSet(request.POST, request.FILES)
        formset.club = crowd.id
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.club = crowd
                instance.save()
            return redirect('/club/' + id + '/')
    return render(request, 'club/announcement.html', context)  

@login_required
@user_is_admin	
def about(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    context['crowd'] = crowd
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    context['form'] = ClubForm(instance=crowd)
    if request.method == 'POST':
        form = ClubForm(request.POST)
        post_info = request.POST
        if form.is_valid():
            updated_crowd = crowd
            updated_crowd.bio = post_info['bio']
            updated_crowd.name = post_info['name']
            updated_crowd.city = post_info['city']
            updated_crowd.state = post_info['state']
            updated_crowd.established = post_info['established']
            updated_crowd.annual_fee = post_info['annual_fee']
            if 'is_public' in post_info:
				updated_crowd.is_public = True
            else:
				updated_crowd.is_public = False
            updated_crowd.save()
            context['form'] = ClubForm(instance=crowd)
            return redirect('/club/' + id + '/')
    return render(request, 'club/about.html', context)  

@login_required
@user_is_admin	
def membership(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    club_user_check = Club_User.objects.filter(club=crowd).exists()
    context['club_user_check'] = club_user_check
    club_pending_user_check = Club_Application.objects.filter(club=crowd).filter(status='pending').exists()
    context['club_pending_user_check'] = club_pending_user_check
    if club_pending_user_check:
		club_pending_user = Club_Application.objects.filter(club=crowd).filter(status='pending')
		context['club_pending_user'] = club_pending_user
    club_inactive_user_check = Club_User.objects.filter(club=crowd).filter(is_active=False).exists()
    context['club_inactive_user_check'] = club_inactive_user_check
    if club_user_check:
		club_user = Club_User.objects.filter(club=crowd)
		context['club_user'] = club_user
    context['crowd'] = crowd
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    if request.method == "POST": 
		rp = request.POST
		if 'inactivate' in rp:
			member_id = request.POST.get("inactivate")
			club_member = Club_User.objects.get(id=member_id, club=crowd)
			club_member.is_active = False
			club_member.save()
			return redirect('/club/' + id + '/manage/membership/')
		elif 'setactive' in rp:
			member_id = request.POST.get("setactive")
			club_member = Club_User.objects.get(id=member_id, club=crowd)
			club_member.is_active = True
			club_member.save()
			return redirect('/club/' + id + '/manage/membership/')
		elif 'removeadmin' in rp:
			member_id = request.POST.get("removeadmin")
			club_member = Club_User.objects.get(id=member_id, club=crowd)
			club_member.is_admin = False
			club_member.save()
			return redirect('/club/' + id + '/manage/membership/')
		elif 'addadmin' in rp:
			member_id = request.POST.get("addadmin")
			club_member = Club_User.objects.get(id=member_id, club=crowd)
			club_member.is_admin = True
			club_member.save()
			return redirect('/club/' + id + '/manage/membership/')
		elif 'acceptpending' in rp:
			member_id = request.POST.get("acceptpending")
			member_object = User.objects.get(id=member_id)
			club_member = Club_Application.objects.get(user=member_object, club=crowd, status='pending')
			club_member.status = 'accepted'
			club_member.date_completed = datetime.datetime.now()
			club_member.save()
			club_user_add = Club_User(user=member_object, club=crowd, is_active=True)
			club_user_add.save()
			return redirect('/club/' + id + '/manage/membership/')
		elif 'rejectpending' in rp:
			member_id = request.POST.get("rejectpending")
			member_object = User.objects.get(id=member_id)
			club_member = Club_Application.objects.get(user=member_object, club=crowd, status='pending')
			club_member.status = 'rejected'
			club_member.date_completed = datetime.datetime.now()
			club_member.save()
			return redirect('/club/' + id + '/manage/membership/')
    return render(request, 'club/membership.html', context)  

@login_required
@user_is_admin	
def event(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    context['crowd'] = crowd
    club_event_check = Club_Event.objects.filter(club=crowd).exists()
    if club_event_check:
		club_event = Club_Event.objects.filter(club=crowd)
		context['club_event'] = club_event
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    return render(request, 'club/event.html', context)

@login_required
def add(request):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    context['form'] = ClubForm()
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            crowd = form.save()
            crowd.is_active = True
            crowd.save()
            club = Club.objects.get(id=crowd.id)
            crowd_user = Club_User(user=user_object, club=club, is_admin=True, is_active=True)
            crowd_user.save()
            return redirect('/club/' + str(crowd.id) + '/')
    return render(request, 'club/add.html', context)

@login_required	
def search(request):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    public_crowds = Club.objects.filter(is_public=True).filter(is_active=True)
    context['public_crowds'] = public_crowds
    return render(request, 'club/search.html', context)
	
@login_required
@user_is_admin
def addevent(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    context['form'] = EventForm(club=id)
    context['crowd'] = crowd
    if request.method == 'POST':
        form = EventEditForm(request.POST)
        if form.is_valid():
            event = form.save()
            event.is_active = True
            event.save()
            event_object = Event.objects.get(id=event.id)
            crowd_event = Club_Event(club=crowd, event=event_object)
            crowd_event.save()
            return redirect('/club/' + str(crowd.id) + '/')
    return render(request, 'club/addevent.html', context)
	
@login_required
@user_is_admin
def newaddress(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    context['form'] = EventAddressForm()
    context['crowd'] = crowd
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    if request.method == 'POST':
        form = EventAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.club = crowd
            address.save()
            return redirect('/club/' + str(crowd.id) + '/manage/event/')
    return render(request, 'club/newaddress.html', context)

@login_required
@user_is_admin
def address(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    event_address = Event_Address.objects.filter(club=crowd)
    context['event_address'] = event_address
    context['crowd'] = crowd
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    return render(request, 'club/address.html', context)  
	
@login_required
@user_is_admin
def editaddress(request, id, address_id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    event_address = Event_Address.objects.get(id=address_id)
    context['form'] = EventAddressEditForm(instance=event_address)
    context['crowd'] = crowd
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    if request.method == 'POST':
        form = EventAddressEditForm(request.POST, instance=event_address)
        if form.is_valid():
            form.save()
            return redirect('/club/' + str(crowd.id) + '/manage/event/')
    return render(request, 'club/editaddress.html', context)