from django.contrib import admin
from .models import Beer_Category, Favorite_Beers, Wanted_Beers, Beer_Rating, Beer_Banner, Beer_Note
# Register your models here.
admin.site.register(Beer_Category)
admin.site.register(Favorite_Beers)
admin.site.register(Wanted_Beers)
admin.site.register(Beer_Rating)
admin.site.register(Beer_Banner)
admin.site.register(Beer_Note)