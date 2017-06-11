from django.contrib import admin
from .models import Event, Event_Address, Event_Beer, Event_Attend

# Register your models here.

admin.site.register(Event)
admin.site.register(Event_Address)
admin.site.register(Event_Beer)
admin.site.register(Event_Attend)