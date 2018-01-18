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
from beerclub.decorators import user_is_admin, event_is_active, user_is_member
from beerclub.utils import navigation, mobile
import operator

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
    event_attend_check = Event_Attend.objects.filter(user=user_object).exists()
    context['event_attend_check'] = event_attend_check
    if event_attend_check:
		context['attending'] = Event_Attend.objects.filter(user=user_object).filter(event__is_active=True).filter(event__event_date__gte=timezone.now()).filter(will_attend=True).order_by('event__event_date').select_related()
		context['attended'] = Event_Attend.objects.filter(user=user_object).filter(event__is_active=True).filter(event__event_date__lt=timezone.now()).filter(will_attend=True).order_by('-event__event_date').select_related()
		context['declining'] = Event_Attend.objects.filter(user=user_object).filter(event__is_active=True).filter(event__event_date__gte=timezone.now()).filter(will_attend=False).order_by('event__event_date').select_related()
		context['declined'] = Event_Attend.objects.filter(user=user_object).filter(event__is_active=True).filter(event__event_date__lt=timezone.now()).filter(will_attend=False).order_by('-event__event_date').select_related()
    if club_check:
		clubs = Club_User.objects.filter(user=user_object).values('club_id')
		context['events'] = Club_Event.objects.filter(club__in=clubs).filter(event__is_active=True).filter(event__event_date__gte=timezone.now()).order_by('event__event_date').select_related()
		context['past_events'] = Club_Event.objects.filter(club__in=clubs).filter(event__is_active=True).filter(event__event_date__lt=timezone.now()).order_by('-event__event_date').select_related()
    return render(request, 'event/index.html', context)  
	

@login_required
@event_is_active
@user_is_member
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
        committed = Event_Beer.objects.filter(event=event, is_active=True).values('bdb_id', 'beer_company', 'beer_name', 'brewery_id', 'beer_category').distinct()
        committed_bdb_id = Event_Beer.objects.filter(event=event, is_active=True).values('bdb_id').distinct()
        beer_score = []
        score_beercrowd = []
        score_club = []
        score_user = []
        for sb in committed:
			score_bdb_id = sb['bdb_id']
			beer_score_check = Beer_Score.objects.filter(bdb_id=score_bdb_id).filter(user=user_object).exists()
			if beer_score_check:
				rating = Beer_Score.objects.get(user=user_object, bdb_id=score_bdb_id)
				beer_score.append(rating)
			else:
				beer_score.append({'bdb_id': sb['bdb_id'], 'brewery_id':sb['brewery_id'], 'user':user_object, 'beer_name':sb['beer_name'], 'beer_category':sb['beer_category'], 'score':0})
			context['beer_score'] = beer_score
			"""
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
		"""
        context['committed'] = committed
        #context['score_user'] = score_user
    desired = []
    event_beer_check = Event_Beer.objects.filter(event=event).filter(is_active=True).exists()
    event_attendance_check = Event_Attend.objects.filter(event=event).filter(user=user_object).exists()
    taster_response_check = Event_Attend.objects.filter(event=event).exists()
    context['taster_response_check'] = taster_response_check
    taster_response_attending_check = Event_Attend.objects.filter(event=event).filter(will_attend=True).exists()
    context['taster_response_attending_check'] = taster_response_attending_check
    event_note_check = Event_Note.objects.filter(event=event).exists()
    context['event_notes'] = {}
    if event_note_check:
		context['event_notes'] = Event_Note.objects.filter(event=event).select_related('user').order_by('-date_added')
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
		elif 'removeconfirmed' in rp:
			event_beer_id = request.POST.get("removeconfirmed")
			confirmed_beer = Event_Beer.objects.filter(bdb_id=event_beer_id)
			for beer_obj in confirmed_beer:
				beer_obj.is_active = False
				beer_obj.save()
			return redirect(redirect_url)
		elif 'assignratings' in rp:
			rating_value = rp['assignratings']
			context['rating_value'] = rating_value
			bdb_id = rp['bdb_id']
			beer_name = rp['beer_name']
			beer_company = rp['beer_company']
			brewery_id = rp['brewery_id']
			beer_category = rp['beer_category']
			beer_score_check = Beer_Score.objects.filter(bdb_id=bdb_id).filter(user=user_object).exists()
			if beer_score_check:
				rating = Beer_Score.objects.get(bdb_id=bdb_id, user=user_object)
				rating.score = rating_value
				rating.save()
				return redirect(redirect_url)
			else:
				new_rating = Beer_Score(user=user_object, bdb_id = bdb_id, score = rating_value, beer_name = beer_name, beer_category = beer_category, beer_company = beer_company, brewery_id = brewery_id)
				new_rating.save()
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
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            post_info = form.save()
            updated_event = event
            updated_event.description = post_info.description
            updated_event.event_name = post_info.event_name
            updated_event.event_date = post_info.event_date
            updated_address = post_info.address
            address = Event_Address.objects.get(id=updated_address.id)
            updated_event.address = address
            updated_event.is_active = post_info.is_active
            updated_event.save()
            if post_info.is_active == True:
				return redirect('/event/' + event_id + '/')
            else:
				return redirect('/club/' + str(club_event.club.id) + '/')
        else:
			context['form'] = form
    return render(request, 'event/manage.html', context)