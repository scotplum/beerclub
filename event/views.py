from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .models import Event, Event_Address, Event_Beer, Event_Attend, Event_Note
from club.models import Club, Club_User, Club_Event
from home.models import Wanted_Beers, Beer_Banner
from django.utils import timezone
from django.utils.timezone import datetime
from forms import EventForm
from beerclub.decorators import user_is_admin

# Create your views here.

context = {}

@login_required
def event(request):
    user_object = request.user
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    context['user_object'] = user_object
    now = timezone.now()
    events = Event.objects.filter(event_date__gte=timezone.now())
    pastevents = Event.objects.filter(event_date__lt=timezone.now())
    context['events'] = events
    context['past_events'] = pastevents
    return render(request, 'event/index.html', context)  
	

@login_required
def one_event(request, event_id):
    user_object = request.user 
    context['user_object'] = user_object
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    event = Event.objects.get(id=event_id)
    context['event'] = event
    club_event = Club_Event.objects.get(event=event)
    context['club_event'] = club_event
    club_admin_check = Club_User.objects.filter(club=club_event.club).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    suggestions = Wanted_Beers.objects.all()
    commited_beer_check = Event_Beer.objects.filter(event=event).exists()
    if commited_beer_check:
        committed = Event_Beer.objects.filter(event=event)
        context['committed'] = committed
    desired = []
    for beer in suggestions:
	    desired.append(beer.beer_name)
    context['suggestions'] = suggestions
    event_beer_check = Event_Beer.objects.filter(event=event).exists()
    event_attendance_check = Event_Attend.objects.filter(event=event).filter(user=user_object).exists()
    taster_response_check = Event_Attend.objects.filter(event=event).exists()
    event_note_check = Event_Note.objects.filter(event=event).exists()
    context['event_notes'] = {}
    if event_note_check:
		context['event_notes'] = Event_Note.objects.filter(event=event)
    context['declined_check'] = Event_Attend.objects.filter(event=event).filter(will_attend=False).exists()
    context['confirmed_check'] = Event_Attend.objects.filter(event=event).filter(will_attend=True).exists()
    suggest = []
    if taster_response_check:
		taster_response = Event_Attend.objects.filter(event=event)
		context['taster_response'] = taster_response
		suggest = []
		for taster in taster_response:
			if taster.will_attend == True:
				want = Wanted_Beers.objects.filter(user=taster.user)
				suggest.append(want)
    if event_attendance_check:
		event_attendance = Event_Attend.objects.get(user=user_object, event=event)
		context['event_attendance'] = event_attendance
    context['suggest'] = suggest
    context['event_attendance_check'] = event_attendance_check
    context['event_beer_check'] = event_beer_check
    redirect_url = '/event/' + event_id + '/'
    if request.method == "POST": 
		rp = request.POST
		if 'remove' in rp:
			event_attend = Event_Attend.objects.get(user=user_object, event=event)
			event_attend.will_attend = False
			user_beer_check = Event_Beer.objects.filter(user=user_object, event=event).exists()
			if user_beer_check:
				user_beer = Event_Beer.objects.filter(user=user_object, event=event)
				for beer in user_beer:
					beer.is_active = False
					beer.save()
			event_attend.save()
			return redirect(redirect_url)
		elif 'activate' in rp:
			event_attend = Event_Attend.objects.get(user=user_object, event=event)
			event_attend.will_attend = True
			user_beer_check = Event_Beer.objects.filter(user=user_object, event=event).exists()
			if user_beer_check:
				user_beer = Event_Beer.objects.filter(user=user_object, event=event)
				for beer in user_beer:
					beer.is_active = True
					beer.save()
			event_attend.save()
			return redirect(redirect_url)
		elif 'attend' in rp:
			event_attend = Event_Attend(user=user_object, event=event, date_added=timezone.now(), will_attend=True,)
			event_attend.save()
			return redirect(redirect_url)
		elif 'decline' in rp:
			event_attend = Event_Attend(user=user_object, event=event, date_added=timezone.now(), will_attend=False,)
			event_attend.save()
			return redirect(redirect_url)
		elif 'eventnote' in rp:
			note = rp['notevalue']
			event_note = Event_Note(user=user_object, event=event, is_active=True, date_added=timezone.now(), note=note,)
			event_note.save()
			return redirect(redirect_url)
    return render(request, 'event/event.html', context)  

@login_required
def newaddress(request, event_id):
    user_object = request.user 
    context['user_object'] = user_object
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    event = Event.objects.get(id=event_id)
    context['event'] = event
    club_event = Club_Event.objects.get(event=event)
    context['club_event'] = club_event
    club_admin_check = Club_User.objects.filter(club=club_event.club).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    return render(request, 'event/newaddress.html', context)

@login_required	
def manage(request, event_id):
    context = {}
    user_object = request.user 
    context['user_object'] = user_object
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    event = Event.objects.get(id=event_id)
    context['event'] = event
    club_event = Club_Event.objects.get(event=event)
    context['club_event'] = club_event
    club_admin_check = Club_User.objects.filter(club=club_event.club).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    context['form'] = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST)
        post_info = request.POST
        if form.is_valid():
            updated_event = event
            updated_event.description = post_info['description']
            updated_event.event_name = post_info['event_name']
            updated_event.event_date = post_info['event_date']
            updated_address = post_info['address']
            address = Event_Address.objects.get(id=updated_address)
            updated_event.address = address
            if 'is_active' in post_info:
				updated_event.is_active = True
            else:
				updated_event.is_active = False
            updated_event.save()
            return redirect('/event/' + event_id + '/')
    return render(request, 'event/manage.html', context)