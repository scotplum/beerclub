from django.contrib import admin
from .models import Club, Club_Admin, Club_User

# Register your models here.

admin.site.register(Club)
admin.site.register(Club_Admin)
admin.site.register(Club_User)