from django.contrib import admin
from .models import Beer_Category, Favorite_Beers, Wanted_Beers, Beer_Rating
# Register your models here.
admin.site.register(Beer_Category)
admin.site.register(Favorite_Beers)
admin.site.register(Wanted_Beers)
admin.site.register(Beer_Rating)