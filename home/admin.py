from django.contrib import admin
from .models import Favorite_Beers, Wanted_Beers, Beer_Rating, Beer_Banner, Beer_Note, Beer_Attribute_Category, Beer_Attribute_Section, Beer_Attribute, Profile_Sheet, Beer_Score, Brewery_Score, Brewery_Note, Beer, Beer_User_Image
# Register your models here.
admin.site.register(Favorite_Beers)
admin.site.register(Wanted_Beers)
admin.site.register(Beer_Rating)
admin.site.register(Beer_Banner)
admin.site.register(Beer_Note)
admin.site.register(Beer_Attribute_Category)
admin.site.register(Beer_Attribute_Section)
admin.site.register(Beer_Attribute)
admin.site.register(Profile_Sheet)
admin.site.register(Beer_Score)
admin.site.register(Brewery_Score)
admin.site.register(Brewery_Note)
admin.site.register(Beer)
admin.site.register(Beer_User_Image)