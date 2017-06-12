from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .models import Event, Event_Address, Event_Beer, Event_Attend, Event_Note
from home.models import Wanted_Beers
from django.utils import timezone
from django.utils.timezone import datetime

# Create your views here.

context = {}

@login_required
def event(request):
    user_object = request.user 
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
    event = Event.objects.get(id=event_id)
    context['event'] = event
    suggestions = Wanted_Beers.objects.all()
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
			event_attend.save()
			return redirect(redirect_url)
		elif 'activate' in rp:
			event_attend = Event_Attend.objects.get(user=user_object, event=event)
			event_attend.will_attend = True
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