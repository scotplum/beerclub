from django.contrib import admin
from .models import Event, Event_Address

# Register your models here.

admin.site.register(Event)
admin.site.register(Event_Address)