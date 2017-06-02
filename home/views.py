from django.shortcuts import render 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .models import Favorite_Beers 
from forms import findbeerForm 
import requests

# Create your views here.

context = {}

@login_required 
def index(request): 
    user_object = request.user 
    context['user_object'] = user_object 
    context['favorite'] = Favorite_Beers.objects.filter(user_id=user_object.id) 
    context['form'] = findbeerForm() 
    return render(request, 'home/index.html', context)  
	
@login_required 
def findbeer(request): 
    user_object = request.user 
    if request.method == "POST": 
        form = findbeerForm(request.POST) 
        if form.is_valid(): 
         
            #Search BreweryDB api for results from user's findbeerForm submission 
            formdata = form.cleaned_data
            secret = '4896533a04534eff709518ee74c57d94' 
            search = formdata['beer'] #? Need to figure out how to get the value from the search 
            beersearch_url = 'http://api.brewerydb.com/v2/search/?withBreweries=Y&key=' + secret + '&q=' + search 
             
            #Retrieve Search Result From BreweryDB 
             
            beersearch = requests.get(beersearch_url).json() 
            context['beersearch'] = beersearch['data']			
            return render(request, 'home/findbeer.html', context) 
    else: 
        form = findbeerForm() 
     
    return render(request, 'home/findbeer.html',{'form':form}) 
