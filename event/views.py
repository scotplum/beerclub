from django.shortcuts import render, redirect
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .models import Event, Event_Address, Event_Beer, Event_Attend, Event_Note
from club.models import Club, Club_User, Club_Event
from home.models import Wanted_Beers, Beer_Banner, Beer_Score
from django.utils import timezone
from django.utils.timezone import datetime
from forms import EventForm, EventEditForm
from beerclub.decorators import user_is_admin, event_is_active
from beerclub.utils import navigation

# Create your views here.

context = {}

@login_required
def event(request):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    club_check = nav['club_check']
    now = timezone.now()
    if club_check:
		clubs = Club_User.objects.filter(user=user_object).select_related()
		club_events = []
		club_past_events = []
		for club in clubs:
			club_object = Club.objects.get(id=club.club.id)
			if Club_Event.objects.filter(club=club_object).filter(event__event_date__gte=timezone.now()).exists():
				events = Club_Event.objects.filter(club=club_object).filter(event__event_date__gte=timezone.now()).select_related()
				club_events.append(events)
			if Club_Event.objects.filter(club=club_object).filter(event__event_date__lt=timezone.now()).exists():
				past_events = Club_Event.objects.filter(club=club_object).filter(event__event_date__lt=timezone.now()).select_related()
				club_past_events.append(past_events)
		context['events'] = club_events
		context['past_events'] = club_past_events
    return render(request, 'event/index.html', context)  
	

@login_required
@event_is_active
def one_event(request, event_id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    event = Event.objects.get(id=event_id)
    context['event'] = event
    club_event = Club_Event.objects.get(event=event)
    context['club_event'] = club_event
    club = club_event.club
    context['club'] = club
    club_admin_check = Club_User.objects.filter(club=club_event.club).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    committed_beer_check = Event_Beer.objects.filter(event=event).exists()
    club_users = Club_User.objects.filter(club=club).values_list('user')
    if committed_beer_check:
        committed = Event_Beer.objects.filter(event=event, is_active=True).values('bdb_id', 'beer_company', 'beer_name').distinct()
        score_beercrowd = []
        score_club = []
        score_user = []
        for sb in committed:
			score_bdb_id = sb['bdb_id']
			score_bc_average = Beer_Score.objects.filter(bdb_id=score_bdb_id).aggregate(Avg('score'))
			score_bc_count = Beer_Score.objects.filter(bdb_id=score_bdb_id).aggregate(Count('score'))
			score_beercrowd.append([score_bdb_id, score_bc_average['score__avg'], score_bc_count['score__count']])
			score_club_average = Beer_Score.objects.filter(bdb_id=score_bdb_id).filter(user__in=club_users).aggregate(Avg('score'))
			score_club_count = Beer_Score.objects.filter(bdb_id=score_bdb_id).filter(user__in=club_users).aggregate(Count('score'))
			score_club.append([score_bdb_id, score_club_average['score__avg'], score_club_count['score__count']])
			score_user_average = Beer_Score.objects.filter(bdb_id=score_bdb_id).filter(user=user_object).aggregate(Avg('score'))
			score_user_count = Beer_Score.objects.filter(bdb_id=score_bdb_id).filter(user=user_object).aggregate(Count('score'))
			score_user.append([score_bdb_id, score_user_average['score__avg'], score_user_count['score__count']])
        context['score_beercrowd'] = score_beercrowd
        context['score_club'] = score_club
        context['committed'] = committed
        context['score_user'] = score_user
    desired = []
    event_beer_check = Event_Beer.objects.filter(event=event).filter(is_active=True).exists()
    event_attendance_check = Event_Attend.objects.filter(event=event).filter(user=user_object).exists()
    taster_response_check = Event_Attend.objects.filter(event=event).exists()
    context['taster_response_check'] = taster_response_check
    event_note_check = Event_Note.objects.filter(event=event).exists()
    context['event_notes'] = {}
    if event_note_check:
		context['event_notes'] = Event_Note.objects.filter(event=event).select_related('user')
    context['declined_check'] = Event_Attend.objects.filter(event=event).filter(will_attend=False).exists()
    context['confirmed_check'] = Event_Attend.objects.filter(event=event).filter(will_attend=True).exists()
    suggest = []
    if taster_response_check:
		taster_response = Event_Attend.objects.filter(event=event).select_related('user', 'event')
		context['taster_response'] = taster_response
		suggest = []
		for taster in taster_response:
			if taster.will_attend == True:
				want = Wanted_Beers.objects.filter(user=taster.user).filter(is_active=True).select_related('user')
				suggest.append(want)
    suggest_distinct = []
    bdb_id = []
    for beer in suggest:
		for b in beer:
			if b.bdb_id not in bdb_id:
				event_wanted_beer = [b.bdb_id, b.beer_company, b.beer_name]
				bdb_id.append(b.bdb_id)
				suggest_distinct.append(event_wanted_beer)
    context['suggest_distinct'] = suggest_distinct
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
		if 'removeconfirmed' in rp:
			event_beer_id = request.POST.get("removeconfirmed")
			confirmed_beer = Event_Beer.objects.filter(bdb_id=event_beer_id)
			for beer_obj in confirmed_beer:
				beer_obj.is_active = False
				beer_obj.save()
			return redirect(redirect_url)
    return render(request, 'event/event.html', context)  

@login_required	
def manage(request, event_id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    event = Event.objects.get(id=event_id)
    context['event'] = event
    club_event = Club_Event.objects.get(event=event)
    context['club_event'] = club_event
    club_admin_check = Club_User.objects.filter(club=club_event.club).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    context['form'] = EventForm(instance=event, club=club_event.club.id)
    if request.method == 'POST':
        form = EventEditForm(request.POST)
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