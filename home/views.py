from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .models import Favorite_Beers, Wanted_Beers, Beer_Rating, Beer_Banner, Beer_Note, BeerNoteForm, Beer_Color, Beer_Head, Profile_Sheet
from event.models import Event, Event_Beer
from forms import findbeerForm, ProfileSheetForm
from star_ratings.models import UserRating, Rating
from django.utils import timezone
import requests

# Create your views here.

context = {}
secret = '4896533a04534eff709518ee74c57d94' 

@login_required 
def index(request): 
    user_object = request.user 
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    beer_notes_check = Beer_Note.objects.filter(user=user_object).exists()
    context['beer_notes_check'] = beer_notes_check
    if beer_notes_check:
		beer_notes = Beer_Note.objects.filter(user=user_object).order_by('-date_added')[:8]
		context['beer_notes'] = beer_notes    
    beer_rating_check = UserRating.objects.filter(user=user_object).exists()
    context['beer_rating_check'] = beer_rating_check
    if beer_rating_check:
		beer_rating = UserRating.objects.filter(user=user_object).order_by('-id')[:12]
		context['beer_rating'] = beer_rating
    context['user_object'] = user_object 
    context['favorite'] = Favorite_Beers.objects.filter(user_id=user_object.id) 
    context['wanted'] = Wanted_Beers.objects.filter(user_id=user_object.id)
    context['form'] = findbeerForm() 
    fav_beer_check = Favorite_Beers.objects.filter(user=user_object).exists()
    want_beer_check = Wanted_Beers.objects.filter(user=user_object).exists()
    context['fav_beer_check'] = fav_beer_check
    context['want_beer_check'] = want_beer_check	
    now = timezone.now()
    events = Event.objects.filter(event_date__gte=timezone.now())
    pastevents = Event.objects.filter(event_date__lt=timezone.now())
    context['events'] = events
    context['past_events'] = pastevents
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
    return render(request, 'home/index.html', context)  
	
@login_required 
def findbeer(request): 
    user_object = request.user 
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    if request.method == "POST": 
        form = findbeerForm(request.POST) 
        if form.is_valid(): 
         
            #Search BreweryDB api for results from user's findbeerForm submission 
            formdata = form.cleaned_data
            search = formdata['beer'] #? Need to figure out how to get the value from the search 
            beersearch_url = 'http://api.brewerydb.com/v2/search/?withBreweries=Y&key=' + secret + '&q=' + search 
             
            #Retrieve Search Result From BreweryDB 
             
            beersearch = requests.get(beersearch_url).json() 
            context['beersearch'] = beersearch['data']			
            return render(request, 'home/findbeer.html', context) 
    else: 
        form = findbeerForm() 
     
    return render(request, 'home/findbeer.html',{'form':form}) 

@login_required
def beer(request, bdb_id):
    user_object = request.user
    urlbeer = 'http://api.brewerydb.com/v2/beer/' + bdb_id + '?withBreweries=Y&key=' + secret
    urlprofilesheet = '/home/findbeer/' + bdb_id + '/profilesheet/'
    context['urlprofilesheet'] = urlprofilesheet
	#Retrieve Beer Using ID From BreweryDB
    beer = requests.get(urlbeer).json()
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
					brewery_website = brew['website']
				if 'locations' in brew:
					for location in brew['locations']:
						if 'region' in location:
							context['region'] = location['region']
    context['data'] = data
    context['style'] = style
    beer_note_check = Beer_Note.objects.filter(bdb_id=bdb_id).filter(user=user_object).exists()
    context['beer_notes'] = {}
    if beer_note_check:
		context['beer_notes'] = Beer_Note.objects.filter(bdb_id=bdb_id).filter(user=user_object)
    beer_rating_check = Beer_Rating.objects.filter(bdb_id=bdb_id).exists()
    fav_beer_check = Favorite_Beers.objects.filter(user=user_object).filter(bdb_id=bdb_id).exists()
    want_beer_check = Wanted_Beers.objects.filter(user=user_object).filter(bdb_id=bdb_id).exists()
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		if image_url:
			beer_banner = Beer_Banner.objects.get(user=user_object)
			beer_banner.image_url = image_url
			beer_banner.beer_website = brewery_website
			beer_banner.save()
    else:
		if image_url:
			beer_banner = Beer_Banner(user=user_object, image_url=image_url, beer_website=brewery_website)
			beer_banner.save()
    beer_banner = Beer_Banner.objects.get(user=user_object)
    context['banner'] = beer_banner
    context['fav_beer_check'] = fav_beer_check
    context['want_beer_check'] = want_beer_check
    context['beer_rating_check'] = beer_rating_check
    if beer_rating_check:
		pass
    else:
		beer_rating = Beer_Rating(beer_company = beer_company, beer_name = beer_name, beer_category = beer_category, date_added=timezone.now(), bdb_id = bdb_id)
		beer_rating.save()
    score_beer = Beer_Rating.objects.get(bdb_id=bdb_id)
    context['score_beer'] = score_beer
    if fav_beer_check is True:
		fav_beer = Favorite_Beers.objects.get(user=user_object, bdb_id=bdb_id)
		context['fav_beer'] = fav_beer
    if want_beer_check is True:
		want_beer = Wanted_Beers.objects.get(user=user_object, bdb_id=bdb_id)
		context['want_beer'] = want_beer
	
	#If the request method is a POST from a form submission then either add or remove from Favorite or Wanted beers
    if request.method == "POST": 
		rp = request.POST
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
def beerevent(request, bdb_id):
    user_object = request.user 
    context['user_object'] = user_object 
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
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
    context['data'] = data
    context['style'] = style
    context['category'] = style['category']
    beer_name = data['name']
    beer_category = style['name']
    if request.method == "POST": 
		rp = request.POST
		for event in events:
			eid = str(event.id)
			if eid in rp:
				event_beer = Event_Beer(user=user_object, event = event, beer_company = beer_company, beer_name = beer_name, beer_category = beer_category, date_added=timezone.now(), is_active=True, bdb_id = bdb_id)
				event_beer.save()
				return redirect('/home/')
			else:
				return render(request, 'fun.html', context)
    return render(request, 'home/beerevent.html', context)

@login_required	
def tasters(request):
    user_object = request.user 
    context['user_object'] = user_object 
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    tasters = User.objects.filter(is_active=True)
    context['tasters'] = tasters
    return render(request, 'home/tasters.html', context)

@login_required	
def taster(request, id):
    context = {}
    user_object = User.objects.get(id=id)
    current_user = request.user
    context['user_object'] = user_object
    beer_banner_check = Beer_Banner.objects.filter(user=current_user).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=current_user)	
		context['banner'] = beer_banner
    fav_beer_check = Favorite_Beers.objects.filter(user=id).exists()
    want_beer_check = Wanted_Beers.objects.filter(user=id).exists()
    context['fav_beer_check'] = fav_beer_check
    context['want_beer_check'] = want_beer_check
    beer_notes_check = Beer_Note.objects.filter(user=user_object).exists()
    context['beer_notes_check'] = beer_notes_check
    if beer_notes_check:
		beer_notes = Beer_Note.objects.filter(user=user_object).order_by('-date_added')[:8]
		context['beer_notes'] = beer_notes    
    beer_rating_check = UserRating.objects.filter(user=user_object).exists()
    context['beer_rating_check'] = beer_rating_check
    if beer_rating_check:
		beer_rating = UserRating.objects.filter(user=user_object).order_by('-id')[:10]
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
    user_object = request.user
    context['user_object'] = user_object
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    beer_rating_check = UserRating.objects.filter(user=user_object).exists()
    context['beer_rating_check'] = beer_rating_check
    test_rating = Beer_Rating.objects.filter(ratings__isnull=False).order_by('ratings__average')
    if beer_rating_check:
		beer_rating = UserRating.objects.filter(user=user_object).order_by('-id')
		context['beer_rating'] = beer_rating
		user_beer_rating = []
		for beer in beer_rating:
			rated_beer = Beer_Rating.objects.get(bdb_id = beer.rating.content_object.bdb_id)
			user_beer_rating.append(rated_beer)
		context['user_beer_ratings'] = user_beer_rating
    return render(request, 'home/ratings.html', context)

@login_required	
def notes(request):
    user_object = request.user
    context['user_object'] = user_object
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    beer_notes_check = Beer_Note.objects.filter(user=user_object).exists()
    context['beer_notes_check'] = beer_notes_check
    if beer_notes_check:
		beer_notes = Beer_Note.objects.filter(user=user_object).order_by('-date_added')
		context['beer_notes'] = beer_notes    
    return render(request, 'home/notes.html', context)

@login_required	
def noteedit(request, id):
    context['update'] = False
    user_object = request.user
    context['user_object'] = user_object
    beer_note = Beer_Note.objects.get(id=id)
    context['form'] = BeerNoteForm(instance=beer_note)
    context['beer_note'] = beer_note
    beer_banner_check = Beer_Banner.objects.filter(user=user_object).exists()
    if beer_banner_check:
		beer_banner = Beer_Banner.objects.get(user=user_object)	
		context['banner'] = beer_banner
    if request.method == 'POST':
        form = BeerNoteForm(request.POST)
        update_note = request.POST.get("note")
        if form.is_valid():
            updated_beer_note = beer_note
            updated_beer_note.note = update_note
            updated_beer_note.save()
            context['update'] = True
            beer_note = Beer_Note.objects.get(id=id)
            context['beer_note'] = beer_note
            context['form'] = BeerNoteForm(instance=beer_note)
            return render(request, 'home/noteedit.html', context)
    else:
        form = BeerNoteForm()
    return render(request, 'home/noteedit.html',context)

@login_required	
def profilesheet(request, bdb_id):
	user_object = request.user
	context['user_object'] = user_object
	beer_info = Beer_Rating.objects.get(bdb_id=bdb_id)
	context['beer_info'] = beer_info
	beer_head_check = Beer_Head.objects.filter(bdb_id=bdb_id).filter(user=user_object).exists()
	if not beer_head_check:
		beer_head_db = Beer_Head(bdb_id=bdb_id, user=user_object)
		beer_head_db.save()
	beer_head = Beer_Head.objects.filter(bdb_id=bdb_id, user=user_object).values()
	beer_head_save = Beer_Head.objects.get(bdb_id=bdb_id, user=user_object)
	for list in beer_head:
		beer_head_iter = list.iteritems()
		beer_head_false = {}
		beer_head_true = {}
		for k, v in beer_head_iter:
			if v is False:
				beer_head_false[k] = v
			elif v is True:
				beer_head_true[k] = v
	test = beer_head_true
	context['beer_head_true'] = beer_head_true
	context['beer_head_false'] = beer_head_false
	beer_head_fields = Beer_Head._meta.get_fields()
	context['beer_head_fields'] = beer_head_fields
	profile_sheet_check = Profile_Sheet.objects.filter(bdb_id=bdb_id, user=user_object).exists()
	if profile_sheet_check:
		form = ProfileSheetForm(instance=Profile_Sheet.objects.get(bdb_id=bdb_id, user=user_object))
	context['form'] = form
	if request.method == "POST": 
		rp = request.POST
		context['rp'] = rp
		if 'remove_head' in rp:
			rp_head = request.POST.get('remove_head')
			head_update = {rp_head : False}
			for upd in head_update:
				setattr(beer_head_save, upd, head_update[upd])
			beer_head_save.save()
			return redirect('/home/findbeer/' + bdb_id + '/profilesheet/')
		elif 'add_head' in rp:
			rp_head = request.POST.get('add_head')
			head_update = {rp_head : True}
			for upd in head_update:
				setattr(beer_head_save, upd, head_update[upd])
			beer_head_save.save()
			return redirect('/home/findbeer/' + bdb_id + '/profilesheet/')
		if 'Feel' in rp:
			rp_feel = request.POST.get('Feel')
			context['rp_feel'] = rp_feel
			return redirect('/home/findbeer/' + bdb_id + '/profilesheet/')
		if 'Carbonation' in rp:
			rp_carbonation = request.POST.get('Carbonation')
			context['rp_carbonation'] = rp_carbonation
			return redirect('/home/findbeer/' + bdb_id + '/profilesheet/')
	return render(request, 'home/profilesheet.html', context)