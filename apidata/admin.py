from django.contrib import admin
from .models import Beer_Category, Beer_Style

# Register your models here.
admin.site.register(Beer_Category)
admin.site.register(Beer_Style)