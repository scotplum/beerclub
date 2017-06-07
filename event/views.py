from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .models import Event, Event_Address
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