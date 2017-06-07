from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .models import Favorite_Beers, Wanted_Beers
from event.models import Event
from forms import findbeerForm
from django.utils import timezone
import requests

# Create your views here.

context = {}
secret = '4896533a04534eff709518ee74c57d94' 

@login_required 
def index(request): 
    user_object = request.user 
    context['user_object'] = user_object 
    context['favorite'] = Favorite_Beers.objects.filter(user_id=user_object.id) 
    context['wanted'] = Wanted_Beers.objects.filter(user_id=user_object.id)
    context['form'] = findbeerForm() 
    now = timezone.now()
    events = Event.objects.filter(event_date__gte=timezone.now())
    pastevents = Event.objects.filter(event_date__lt=timezone.now())
    context['events'] = events
    context['past_events'] = pastevents
    return render(request, 'home/index.html', context)  
	
@login_required 
def findbeer(request): 
    user_object = request.user 
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
	
	#Retrieve Beer Using ID From BreweryDB
	beer = requests.get(urlbeer).json()
	data = beer['data']
	style = data['style']
	brewery = data['breweries']
	for brew in brewery:
		context['brewery'] = brew
		beer_company = brew['name']
	context['data'] = data
	context['style'] = style
	context['category'] = style['category']
	beer_name = data['name']
	beer_category = style['name']
	fav_beer_check = Favorite_Beers.objects.filter(user=user_object).filter(bdb_id=bdb_id).exists()
	want_beer_check = Wanted_Beers.objects.filter(user=user_object).filter(bdb_id=bdb_id).exists()
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
		if 'fav' in rp:
			favorite_beer = Favorite_Beers(user=user_object, beer_company = beer_company, beer_name = beer_name, beer_category = beer_category, date_added=timezone.now(), is_active=True, bdb_id = bdb_id)
			favorite_beer.save()
			return redirect('/home/')
		elif 'want' in rp:
			want_beer = Wanted_Beers(user=user_object, beer_company = beer_company, beer_name = beer_name, beer_category = beer_category, date_added=timezone.now(), is_active=True, bdb_id = bdb_id)
			want_beer.save()
			return redirect('/home/')
		elif 'removefav' in rp:
			fav_beer.is_active = False
			fav_beer.save()
			#remove_fav = 
			return redirect('/home/')
		elif 'removewant' in rp:
			want_beer.is_active = False
			want_beer.save()
			return redirect('/home/')
		elif 'activatefav' in rp:
			fav_beer.is_active = True
			fav_beer.save()
			return redirect('/home/')
		elif 'activatewant' in rp:
			want_beer.is_active = True
			want_beer.save()
			return redirect('/home/')
		else:
			return render(request, 'home/beer.html', context)
	return render(request, 'home/beer.html', context)