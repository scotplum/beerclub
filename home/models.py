from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating

# Create your models here.
class Beer_Category(models.Model):
	category_name	= models.CharField(max_length=50)
	date_created 	= models.DateTimeField(auto_now_add=True)
	description		= models.CharField(max_length=1000)
	is_active		= models.BooleanField(default=True)
	
	def __str__(self):
		return self.category_name + " | Is Active: " + str(self.is_active)

class Favorite_Beers(models.Model):
	user	 		= models.ForeignKey(User, on_delete=models.CASCADE)
	beer_company 	= models.CharField(max_length=100)
	beer_name		= models.CharField(max_length=500)
	beer_category	= models.CharField(max_length=100)
	date_added	 	= models.DateTimeField(auto_now_add=True)
	is_active 		= models.BooleanField(default=True)
	bdb_id          = models.CharField(max_length=20)
	
	def __str__(self):
		return "beer_name: " + self.beer_name + " | beer_company: " + self.beer_company + " | user: " + str(self.user)
		
class Wanted_Beers(models.Model): 
    user    		= models.ForeignKey(User, on_delete=models.CASCADE) 
    beer_company  	= models.CharField(max_length=100) 
    beer_name  		= models.CharField(max_length=500) 
    beer_category 	= models.CharField(max_length=100)
    date_added   	= models.DateTimeField(auto_now_add=True) 
    is_active   	= models.BooleanField(default=True) 
    bdb_id          = models.CharField(max_length=20) 
     
    def __str__(self): 
		return "beer_name: " + self.beer_name + " | beer_company: " + self.beer_company + " | user: " + str(self.user)
		
class Beer_Rating(models.Model):
    bdb_id          = models.CharField(max_length=20) 
    date_added   	= models.DateTimeField(auto_now_add=True) 
    beer_company  	= models.CharField(max_length=100) 
    beer_name  		= models.CharField(max_length=500) 
    beer_category 	= models.CharField(max_length=100)
    ratings = GenericRelation(Rating, related_query_name='Beer_Rating')
	
    def __str__(self):
		return self.beer_name + ' | ' + self.beer_company
		
class Beer_Banner(models.Model):
    user    		= models.ForeignKey(User, on_delete=models.CASCADE) 
    image_url		= models.URLField(max_length=250)
    beer_website	= models.URLField(max_length=250)
    
    def __str__(self):
		return str(self.user) + ' | ' + self.image_url