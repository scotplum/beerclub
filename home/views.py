from django.shortcuts import render, redirect
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .models import Favorite_Beers, Beer_Score, Wanted_Beers, Beer_Banner, Beer_Note, BeerNoteForm, Profile_Sheet, Beer_Attribute, Beer_Attribute_Section, Beer_Attribute_Category
from event.models import Event, Event_Beer, Event_Attend
from club.models import Club, Club_User, Club_Event
from forms import findbeerForm, ProfileSheetForm, ProfileForm
from django.utils import timezone
import requests
from django.forms import inlineformset_factory
from beerclub.utils import navigation, beerscore
from decouple import config

# Create your views here.

context = {}
secret = config('BREWERYDB')

@login_required 
def index(request): 
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    club_check = nav['club_check']
    context = nav['context']
    beer_notes_check = Beer_Note.objects.filter(user=user_object).filter(is_active=True).exists()
    context['beer_notes_check'] = beer_notes_check
    if beer_notes_check:
		beer_notes = Beer_Note.objects.filter(user=user_object).filter(is_active=True).order_by('-date_added')[:8].select_related()
		context['beer_notes'] = beer_notes    
    beer_rating_check = Beer_Score.objects.filter(user=user_object).exists()
    context['beer_rating_check'] = beer_rating_check
    if beer_rating_check:
		beer_rating = Beer_Score.objects.filter(user=user_object).select_related().order_by('-id')[:12]
		context['beer_rating'] = beer_rating
    context['favorite'] = Favorite_Beers.objects.filter(user_id=user_object.id).select_related()
    context['wanted'] = Wanted_Beers.objects.filter(user_id=user_object.id).select_related()
    context['form'] = findbeerForm() 
    fav_beer_check = Favorite_Beers.objects.filter(user=user_object).exists()
    want_beer_check = Wanted_Beers.objects.filter(user=user_object).exists()
    context['fav_beer_check'] = fav_beer_check
    context['want_beer_check'] = want_beer_check	
    now = timezone.now()
    attribute_trophy_check = Profile_Sheet.objects.filter(user=user_object).filter(beer_attribute__section_id=21).exists()
    context['attribute_trophy_check'] = attribute_trophy_check
    event_attend_check = Event_Attend.objects.filter(user=user_object).exists()
    context['event_attend_check'] = event_attend_check
    if attribute_trophy_check:
		attribute_trophy = Profile_Sheet.objects.filter(user=user_object).filter(beer_attribute__section_id=21).select_related()
		context['attribute_trophy'] = attribute_trophy
		context['trophy_beers'] = attribute_trophy.values_list('bdb_id', 'beer_attribute')
    if event_attend_check:
		context['events'] = Event_Attend.objects.filter(user=user_object).filter(event__is_active=True).filter(event__event_date__gte=timezone.now()).filter(will_attend=True).order_by('event__event_date').select_related()
		context['past_events'] = Event_Attend.objects.filter(user=user_object).filter(event__is_active=True).filter(event__event_date__lt=timezone.now()).filter(will_attend=True).order_by('-event__event_date').select_related()
    if request.method == "POST": 
		rp = request.POST
		if 'removefav' in rp:
			bdb_id = request.POST.get("removefav")
			fav_beer = Favorite_Beers.objects.get(user=user_object, bdb_id=bdb_id)
			fav_beer.is_active = False
			fav_beer.save()
			return redirect('/home/')
		elif 'removewant' in rp:
			bdb_id = request.POST.get("removewant")
			want_beer = Wanted_Beers.objects.get(user=user_object, bdb_id=bdb_id)
			want_beer.is_active = False
			want_beer.save()
			return redirect('/home/')
		elif 'assignratings' in rp:
			rating_value = rp['assignratings']
			ratingvalue, ratingbeer = rating_value.split("_")
			rating = Beer_Score.objects.get(user=user_object, bdb_id=ratingbeer)
			rating.score = ratingvalue
			rating.save()
			return redirect('/home/')
    return render(request, 'home/index.html', context)  
	
@login_required 
def findbeer(request): 
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    if request.method == "POST": 
        rp = request.POST
        context['rp'] = rp
        if 'findbeer' in rp: 
         
            #Search BreweryDB api for results from user's findbeerForm submission 
            formdata = request.POST.get("findbeer")
            search = formdata
            beersearch_url = 'http://api.brewerydb.com/v2/search/?withBreweries=Y&key=' + secret + '&q=' + search 
             
            #Retrieve Search Result From BreweryDB 
             
            beersearch = requests.get(beersearch_url).json()
            if 'data' in beersearch:
				context['beersearch'] = beersearch['data']
            else:
				context['beersearch'] = 'No Beer'
            return render(request, 'home/findbeer.html', context) 
    else: 
        form = findbeerForm() 
     
    return render(request, 'home/findbeer.html') 

@login_required
def beer(request, bdb_id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    beercrowd_score_check = Beer_Score.objects.filter(bdb_id=bdb_id).exists()
    if beercrowd_score_check:
		beercrowd_score = Beer_Score.objects.filter(bdb_id=bdb_id).aggregate(Avg('score'))
		context['beercrowd_score'] = beercrowd_score['score__avg']
		beercrowd_count = Beer_Score.objects.filter(bdb_id=bdb_id).aggregate(Count('score'))
		context['beercrowd_count'] = beercrowd_count['score__count']
    if context['club_check']:
		clubs = context['clubs']
		club_score = beerscore(request, user_object, clubs, bdb_id)
		context['club_score'] = club_score
    urlbeer = 'http://api.brewerydb.com/v2/beer/' + bdb_id + '?withBreweries=Y&key=' + secret
    urlprofilesheet = '/home/findbeer/' + bdb_id + '/profilesheet/'
    context['urlprofilesheet'] = urlprofilesheet
	#Retrieve Beer Using ID From BreweryDB
    beer = requests.get(urlbeer).json()
    context['brewerydb_call'] = beer
    image_url = {}
    data = ''
    style = ''
    brewery = ''
    if 'data' in beer:
		data = beer['data']
		if 'style' in data: 
			style = data['style']
			if 'category' in style:
				beer_category = style['name']
				context['category'] = style['category']
		if 'name' in data:
			beer_name = data['name']
		if 'breweries' in data:
			brewery = data['breweries']
			for brew in brewery:
				context['brewery'] = brew
				if brew['nameShortDisplay']:
					beer_company = brew['nameShortDisplay']
				else: 
					beer_company = brew['name']
				if 'images' in brew:
					brewery_images = brew['images']
					image_url = brewery_images['medium']
				if 'website' in brew:
					brewery_website = brew['website']
				if 'locations' in brew:
					for location in brew['locations']:
						if 'region' in location:
							context['region'] = location['region']
    context['data'] = data
    context['style'] = style
    beer_attribute_check = Profile_Sheet.objects.filter(bdb_id=bdb_id).filter(user=user_object).exists()
    context['beer_attribute_check'] = beer_attribute_check
    attribute_overrall_check = Profile_Sheet.objects.filter(bdb_id=bdb_id).filter(user=user_object).filter(beer_attribute__section_id=20).exists()
    context['attribute_overrall_check'] = attribute_overrall_check
    if attribute_overrall_check:
		attribute_overrall = Profile_Sheet.objects.filter(bdb_id=bdb_id).filter(user=user_object).filter(beer_attribute__section_id=20).select_related()
		context['attribute_overrall'] = attribute_overrall
    if beer_attribute_check:
		profile_sheet = Profile_Sheet.objects.filter(bdb_id=bdb_id, user=user_object)
		ps_attribute = profile_sheet.values_list('beer_attribute')
		ps_attribute_objects = Beer_Attribute.objects.filter(id__in=ps_attribute).prefetch_related('section').order_by('section')
		context['profile_sheet'] = profile_sheet
		context['ps_attribute'] = ps_attribute
		context['ps_attribute_objects'] = ps_attribute_objects
    beer_note_check = Beer_Note.objects.filter(bdb_id=bdb_id).filter(user=user_object).exists()
    context['beer_notes'] = {}
    if beer_note_check:
		context['beer_notes'] = Beer_Note.objects.filter(bdb_id=bdb_id).filter(user=user_object)
    beer_score_check = Beer_Score.objects.filter(user=user_object, bdb_id=bdb_id).exists()
    if beer_score_check:
		rating = Beer_Score.objects.get(user=user_object, bdb_id=bdb_id)
		context['rating'] = rating
    else:
		context['rating'] = 0
    fav_beer_check = Favorite_Beers.objects.filter(user=user_object).filter(bdb_id=bdb_id).exists()
    want_beer_check = Wanted_Beers.objects.filter(user=user_object).filter(bdb_id=bdb_id).exists()
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		if 'image_url' in locals() and 'brewery_website' in locals():
			beer_banner = Beer_Banner.objects.get(user=user_object)
			beer_banner.image_url = image_url
			beer_banner.beer_website = brewery_website
			beer_banner.save()
		elif 'image_url' in locals():
			beer_banner = Beer_Banner.objects.get(user=user_object)
			beer_banner.image_url = image_url
			beer_banner.beer_website = 'no website'
			beer_banner.save()
		else:
			beer_banner = Beer_Banner.objects.get(user=user_object)
			beer_banner.image_url = 'no url'
			beer_banner.beer_website = 'no website'
			beer_banner.save()
    else:
		if 'image_url' in locals() and 'brewery_website' in locals():
			beer_banner = Beer_Banner(user=user_object, image_url=image_url, beer_website=brewery_website)
			beer_banner.save()
		elif 'image_url' in locals():
			beer_banner = Beer_Banner(user=user_object, image_url=image_url, beer_website='no website')
			beer_banner.save()
		else:
			beer_banner = Beer_Banner(user=user_object, image_url='no url', beer_website='no website')
			beer_banner.save()
    beer_banner = Beer_Banner.objects.get(user=user_object)
    context['banner'] = beer_banner
    context['fav_beer_check'] = fav_beer_check
    context['want_beer_check'] = want_beer_check
    if fav_beer_check is True:
		fav_beer = Favorite_Beers.objects.get(user=user_object, bdb_id=bdb_id)
		context['fav_beer'] = fav_beer
    if want_beer_check is True:
		want_beer = Wanted_Beers.objects.get(user=user_object, bdb_id=bdb_id)
		context['want_beer'] = want_beer
	#If the request method is a POST from a form submission then either add or remove from Favorite or Wanted beers
    if request.method == "POST": 
		rp = request.POST
		if 'assignratings' in rp:
			rating_value = rp['assignratings']
			context['rating_value'] = rating_value
			if beer_score_check:
				rating.score = rating_value
				rating.save()
				return redirect('/home/findbeer/' + bdb_id + '/')
			else:
				new_rating = Beer_Score(user=user_object, bdb_id = bdb_id, score = rating_value, beer_name = beer_name, beer_category = beer_category, beer_company = beer_company)
				new_rating.save()
				return redirect('/home/findbeer/' + bdb_id + '/')
		if 'fav' in rp:
			favorite_beer = Favorite_Beers(user=user_object, beer_company = beer_company, beer_name = beer_name, beer_category = beer_category, date_added=timezone.now(), is_active=True, bdb_id = bdb_id)
			favorite_beer.save()
			return redirect('/home/findbeer/' + bdb_id + '/')
		elif 'want' in rp:
			want_beer = Wanted_Beers(user=user_object, beer_company = beer_company, beer_name = beer_name, beer_category = beer_category, date_added=timezone.now(), is_active=True, bdb_id = bdb_id)
			want_beer.save()
			return redirect('/home/findbeer/' + bdb_id + '/')
		elif 'removefav' in rp:
			fav_beer.is_active = False
			fav_beer.save()
			#remove_fav = 
			return redirect('/home/findbeer/' + bdb_id + '/')
		elif 'removewant' in rp:
			want_beer.is_active = False
			want_beer.save()
			return redirect('/home/findbeer/' + bdb_id + '/')
		elif 'activatefav' in rp:
			fav_beer.is_active = True
			fav_beer.save()
			return redirect('/home/findbeer/' + bdb_id + '/')
		elif 'activatewant' in rp:
			want_beer.is_active = True
			want_beer.save()
			return redirect('/home/findbeer/' + bdb_id + '/')
		elif 'beernote' in rp:
			note = rp['beernotevalue']
			beer_note = Beer_Note(user=user_object, bdb_id=bdb_id, is_active=True, date_added=timezone.now(), note=note, beer_name = beer_name, beer_company = beer_company, beer_category = beer_category,)
			beer_note.save()
			return redirect('/home/findbeer/' + bdb_id + '/')
		elif 'event' in rp:
			return redirect('/home/findbeer/' + bdb_id + '/event/')
		else:
			return render(request, 'home/beer.html', context)
    return render(request, 'home/beer.html', context)

@login_required
def profile(request):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    context['form'] = ProfileForm(instance=user_object)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        post_info = request.POST
        if form.is_valid():
            updated_user = user_object
            updated_user.first_name = post_info['first_name']
            updated_user.last_name = post_info['last_name']
            updated_user.email = post_info['email']
            updated_user.save()
            return redirect('/home/profile')
    return render(request, 'home/profile.html', context) 
	
@login_required	
def beerevent(request, bdb_id):
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    urlbeer = 'http://api.brewerydb.com/v2/beer/' + bdb_id + '?withBreweries=Y&key=' + secret
    now = timezone.now()
    events = Event.objects.filter(event_date__gte=timezone.now())
    context['events'] = events
	
	#Retrieve Beer Using ID From BreweryDB
    
    beer = requests.get(urlbeer).json()
    data = beer['data']
    style = data['style']
    brewery = data['breweries']
    for brew in brewery:
		context['brewery'] = brew
		if brew['nameShortDisplay']:
			beer_company = brew['nameShortDisplay']
		else: 
			beer_company = brew['name']
    if data:
		context['data'] = data
		context['style'] = style
		context['category'] = style['category']
		beer_name = data['name']
		beer_category = style['name']
    else:
		context['data'] = 'We could not locate your beer'
    if request.method == "POST": 
		rp = request.POST
		for event in events:
			eid = str(event.id)
			if eid in rp:
				event_beer = Event_Beer(user=user_object, event = event, beer_company = beer_company, beer_name = beer_name, beer_category = beer_category, date_added=timezone.now(), is_active=True, bdb_id = bdb_id)
				event_beer.save()
				return redirect('/event/' + str(event.id) + '/')
    return render(request, 'home/beerevent.html', context)

@login_required	
def tasters(request):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    tasters = User.objects.filter(is_active=True)
    context['tasters'] = tasters
    return render(request, 'home/tasters.html', context)

@login_required	
def taster(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    taster = User.objects.get(id=id)
    context['taster'] = taster
    fav_beer_check = Favorite_Beers.objects.filter(user=id).exists()
    want_beer_check = Wanted_Beers.objects.filter(user=id).exists()
    context['fav_beer_check'] = fav_beer_check
    context['want_beer_check'] = want_beer_check
    beer_notes_check = Beer_Note.objects.filter(user=taster).exists()
    context['beer_notes_check'] = beer_notes_check
    if beer_notes_check:
		beer_notes = Beer_Note.objects.filter(user=taster).order_by('-date_added')[:8]
		context['beer_notes'] = beer_notes    
    beer_rating_check = Beer_Score.objects.filter(user=taster).exists()
    context['beer_rating_check'] = beer_rating_check
    if beer_rating_check:
		beer_rating = Beer_Score.objects.filter(user=taster).order_by('-id')[:10]
		context['beer_rating'] = beer_rating
    if fav_beer_check is True:
		fav_beer = Favorite_Beers.objects.filter(user=id)
		context['fav_beer'] = fav_beer
    if want_beer_check is True:
		want_beer = Wanted_Beers.objects.filter(user=id)
		context['want_beer'] = want_beer
    return render(request, 'home/taster.html', context)

"""	 Code not used currently....replaced by ratings() potentially
def beerscore(request, bdb_id):
    user_object = request.user
    context['user_object'] = user_object
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    beer_rating_check = Beer_Rating.objects.filter(user=user_object).filter(bdb_id=bdb_id).exists()
    context['beer_rating_check'] = beer_rating_check
    if beer_rating_check:
		pass
    else:
		beer_rating = Beer_Rating(user=user_object, date_added=timezone.now(), bdb_id = bdb_id)
		beer_rating.save()
    score_beer = Beer_Rating.objects.get(user=user_object, bdb_id=bdb_id)
    context['score_beer'] = score_beer
    return render(request, 'home/beerscore.html', context)
"""

@login_required	
def ratings(request):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    context['rp'] = 'All'
    attribute_trophy_check = Profile_Sheet.objects.filter(user=user_object).filter(beer_attribute__section_id=21).exists()
    context['attribute_trophy_check'] = attribute_trophy_check
    if attribute_trophy_check:
		attribute_trophy = Profile_Sheet.objects.filter(user=user_object).filter(beer_attribute__section_id=21).select_related()
		context['attribute_trophy'] = attribute_trophy
		context['trophy_beers'] = attribute_trophy.values_list('bdb_id', 'beer_attribute')
    beer_rating_check = Beer_Score.objects.filter(user=user_object).exists()
    context['beer_rating_check'] = beer_rating_check
    if beer_rating_check:
		beer_rating = Beer_Score.objects.filter(user=user_object).select_related().order_by('-score')
		context['beer_rating'] = beer_rating
    if request.method == "POST": 
		rp = request.POST.get("sortratings")
		context['rp'] = rp
		if rp == 'All':
			beer_rating = Beer_Score.objects.filter(user=user_object).order_by('-score')
		elif rp == 'Brewery':
			beer_rating = Beer_Score.objects.filter(user=user_object).order_by('beer_company', 'beer_name')
		elif rp == 'Beer':
			beer_rating = Beer_Score.objects.filter(user=user_object).order_by('beer_name')
		else:
			beer_rating = Beer_Score.objects.filter(user=user_object).filter(score=rp).order_by('beer_name')
		context['beer_rating'] = beer_rating
		return render(request, 'home/ratings.html', context)
    return render(request, 'home/ratings.html', context)

@login_required	
def notes(request):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    attribute_trophy_check = Profile_Sheet.objects.filter(user=user_object).filter(beer_attribute__section_id=21).exists()
    context['attribute_trophy_check'] = attribute_trophy_check
    if attribute_trophy_check:
		attribute_trophy = Profile_Sheet.objects.filter(user=user_object).filter(beer_attribute__section_id=21).select_related()
		context['attribute_trophy'] = attribute_trophy
		context['trophy_beers'] = attribute_trophy.values_list('bdb_id', 'beer_attribute')
    beer_notes_check = Beer_Note.objects.filter(user=user_object).exists()
    context['beer_notes_check'] = beer_notes_check
    context['sort_type'] = 'Most Recent'
    if beer_notes_check:
		beer_notes = Beer_Note.objects.filter(user=user_object).order_by('-date_added')
		context['beer_notes'] = beer_notes
		context['sort_type'] = 'Most Recent'
    if request.method == "POST": 
		rp = request.POST.get("sortnotes")
		context['rp'] = rp
		if rp == 'Most Recent':
			beer_notes = Beer_Note.objects.filter(user=user_object).order_by('-date_added')
			context['beer_notes'] = beer_notes
			context['sort_type'] = 'Most Recent'
		elif rp == 'Beer':
			beer_notes = Beer_Note.objects.filter(user=user_object).order_by('beer_name')
			context['beer_notes'] = beer_notes
			context['sort_type'] = 'Beer'
		elif rp == 'Brewery':
			beer_notes = Beer_Note.objects.filter(user=user_object).order_by('beer_company', 'beer_name')
			context['beer_notes'] = beer_notes
			context['sort_type'] = 'Brewery'
		elif rp == 'Oldest':
			beer_notes = Beer_Note.objects.filter(user=user_object).order_by('date_added')
			context['beer_notes'] = beer_notes
			context['sort_type'] = 'Oldest'
		return render(request, 'home/notes.html', context)
    return render(request, 'home/notes.html', context)

@login_required	
def noteedit(request, id):
    context = {}
    context['update'] = False
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    beer_note = Beer_Note.objects.get(id=id)
    context['form'] = BeerNoteForm(instance=beer_note)
    context['beer_note'] = beer_note
    if request.method == 'POST':
        form = BeerNoteForm(request.POST)
        update_note = request.POST.get("note")
        post_info = request.POST
        if 'removenote' in post_info:
			updated_beer_note = beer_note
			updated_beer_note.is_active = False
			updated_beer_note.save()
			return redirect('/home/')
        if form.is_valid():
            updated_beer_note = beer_note
            updated_beer_note.note = update_note
            updated_beer_note.save()
            context['update'] = True
            beer_note = Beer_Note.objects.get(id=id)
            context['beer_note'] = beer_note
            context['form'] = BeerNoteForm(instance=beer_note)
            return redirect('/home/findbeer/' + beer_note.bdb_id + '/')
    else:
        form = BeerNoteForm()
    return render(request, 'home/noteedit.html',context)

@login_required	
def profilesheet(request, bdb_id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    profile_sheet_check = Profile_Sheet.objects.filter(bdb_id=bdb_id, user=user_object).exists()
    if profile_sheet_check:
		p_s = Profile_Sheet.objects.filter(bdb_id=bdb_id, user=user_object).select_related()
		p_s_a = Profile_Sheet.objects.get(bdb_id=bdb_id, user=user_object)
		ps_attribute = p_s.values_list('beer_attribute', flat=True)
		context['ps_attribute'] = ps_attribute
    else:
		new_p_s = Profile_Sheet.objects.create(bdb_id=bdb_id, user=user_object)
		new_p_s.save()
		p_s = Profile_Sheet.objects.filter(bdb_id=bdb_id, user=user_object).select_related()
		p_s_a = Profile_Sheet.objects.get(bdb_id=bdb_id, user=user_object)
		ps_attribute = p_s.values_list('beer_attribute', flat=True)
		context['ps_attribute'] = ps_attribute
    context['p_s'] = p_s
    beer_info_check = Beer_Score.objects.filter(bdb_id=bdb_id, user=user_object).exists()
    if beer_info_check:
		beer_info = Beer_Score.objects.get(bdb_id=bdb_id, user=user_object)
		context['beer_info'] = beer_info
    profile_section = Beer_Attribute_Section.objects.all().prefetch_related('category')
    context['profile_section'] = profile_section
    profile_category = Beer_Attribute_Category.objects.all()
    context['profile_category'] = profile_category
    profile_attribute = Beer_Attribute.objects.all().prefetch_related('section')
    context['profile_attribute'] = profile_attribute
    if request.method == "POST": 
		rp = request.POST
		context['rp'] = rp
		rp_checks = request.POST.getlist('checks[]')
		context['rp_checks'] = rp_checks
		p_s_a.beer_attribute.clear()
		for a_id in rp_checks:
			attribute_add = Beer_Attribute.objects.get(id=a_id)
			p_s_a.beer_attribute.add(attribute_add)
		p_s_a.save()
		return redirect('/home/findbeer/' + bdb_id + '/')
    return render(request, 'home/profilesheet.html', context)