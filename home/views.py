from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Favorite_Beers

# Create your views here.

context = {}

@login_required
def index(request):
	user_object = request.user
	context['user_object'] = user_object
	context['favorite'] = Favorite_Beers.objects.filter(user_id=user_object.id)
	return render(request, 'home/index.html', context)	