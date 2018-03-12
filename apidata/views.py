from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from .models import Beer_Category, Beer_Style
from decouple import config
import requests

secret = config('BREWERYDB')
context = {}

# Create your views here.

@user_passes_test(lambda u: u.is_superuser, redirect_field_name='/home/')
def update(request):
    context['update_message'] = 'Select the api update you would like to perform'
    if request.method == "POST":
		rp = request.POST
		if 'updatecategory' in rp: 
			bdb_category_api_url = "https://api.brewerydb.com/v2/categories/?key=" + secret + "&format=json"
			bdb_category_api_call = requests.get(bdb_category_api_url).json()
			bdb_categories = bdb_category_api_call['data']
			for category in bdb_categories:
				category_id = category['id']
				category_name = category['name']
				category_add_date = category['createDate']
				category_db_check = Beer_Category.objects.filter(category_bdb_id=category_id).exists()
				if category_db_check:
					context['update_message'] = 'No Category Updates At This Time'
				else:
					beer_category = Beer_Category(name=category_name, category_bdb_id=category_id, create_date=category_add_date)
					beer_category.save()
					context['update_message'] = 'Category Data Updated'
		if 'updatestyle' in rp: 
			bdb_style_api_url = "https://api.brewerydb.com/v2/styles/?key=" + secret + "&format=json"
			bdb_style_api_call = requests.get(bdb_style_api_url).json()
			bdb_styles = bdb_style_api_call['data']
			for style in bdb_styles:
				style_id = style.get('id')
				style_db_check = Beer_Style.objects.filter(style_bdb_id=style_id).exists()
				if style_db_check:
					context['update_message'] = 'No Style Updates At This Time'
				else:
					style_name = style.get('name')
					style_add_date = style.get('createDate')
					style_update_date = style.get('updateDate')
					style_description = style.get('description')
					style_ibuMin = style.get('ibuMin')
					style_ibuMax = style.get('ibuMax')
					style_abvMin = style.get('abvMin')
					style_abvMax = style.get('abvMax')
					style_srmMin = style.get('srmMin')
					style_srmMax = style.get('srmMax')
					style_ogMin = style.get('ogMin')
					style_ogMax = style.get('ogMax')
					style_fgMin = style.get('fgMin')
					style_fgMax = style.get('fgMax')
					style_category_id = style.get('categoryId')
					style_category = Beer_Category.objects.get(category_bdb_id=style_category_id)
					beer_style = Beer_Style(name=style_name, style_bdb_id=style_id, create_date=style_add_date, update_date=style_update_date, description=style_description, ibuMin=style_ibuMin, ibuMax=style_ibuMax, abvMin=style_abvMin, abvMax=style_abvMax, srmMin=style_srmMin, srmMax=style_srmMax, ogMin=style_ogMin, ogMax=style_ogMax, fgMin=style_fgMin, fgMax=style_fgMax, category=style_category)
					beer_style.save()
					context['update_message'] = 'Style Data Updated'
    return render(request, 'apidata/update.html', context)