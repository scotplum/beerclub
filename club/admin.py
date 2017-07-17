from django.contrib import admin
from .models import Club, Club_Admin, Club_User, Club_Announcement, Club_Event

# Register your models here.

admin.site.register(Club)
admin.site.register(Club_Admin)
admin.site.register(Club_User)
admin.site.register(Club_Announcement)
admin.site.register(Club_Event)