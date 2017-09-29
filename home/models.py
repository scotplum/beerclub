from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.forms import ModelForm

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
    
	class Meta:
		ordering = ['beer_name']
	
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
    
    class Meta:
		ordering = ['beer_name']
	
    def __str__(self): 
		return "beer_name: " + self.beer_name + " | beer_company: " + self.beer_company + " | user: " + str(self.user)
		
class Beer_Rating(models.Model):
    bdb_id          = models.CharField(max_length=20) 
    date_added   	= models.DateTimeField(auto_now_add=True) 
    beer_company  	= models.CharField(max_length=100) 
    beer_name  		= models.CharField(max_length=500) 
    beer_category 	= models.CharField(max_length=100)
    ratings 		= GenericRelation(Rating, related_query_name='Beer_Rating')
	
    def __str__(self):
		return self.beer_name + ' | ' + self.beer_company
		
class Beer_Banner(models.Model):
    user    		= models.ForeignKey(User, on_delete=models.CASCADE) 
    image_url		= models.URLField(max_length=250)
    beer_website	= models.URLField(max_length=250)
    
    def __str__(self):
		return str(self.user) + ' | ' + self.image_url
		
class Beer_Note(models.Model):
	user	 		= models.ForeignKey(User, on_delete=models.CASCADE)
	bdb_id          = models.CharField(max_length=20) 
	is_active		= models.BooleanField(default=True)
	date_added		= models.DateTimeField(auto_now_add=True)
	note			= models.TextField(max_length=1000)
	beer_name		= models.CharField(max_length=500)
	beer_company	= models.CharField(max_length=500)
	beer_category	= models.CharField(max_length=100)
	
	def __str__(self):
		return str(self.user) + ' | ' + str(self.bdb_id) + ' | ' + str(self.note)
		
class BeerNoteForm(ModelForm):
    class Meta:
        model = Beer_Note
        fields = ['note']
		
class Beer_Color(models.Model):
	user	 		= models.ForeignKey(User, on_delete=models.CASCADE)	
	bdb_id			= models.CharField(max_length=20)
	
	def __str__(self):
		return str(self.user) + ' | ' + str(self.bdb_id)
		
class Beer_Head(models.Model):
	user	 		= models.ForeignKey(User, on_delete=models.CASCADE)	
	bdb_id			= models.CharField(max_length=20)
	persistent 		= models.BooleanField(default=False)
	rocky 			= models.BooleanField(default=False)
	large 			= models.BooleanField(default=False)
	fluffy 			= models.BooleanField(default=False)
	dissipating 	= models.BooleanField(default=False)
	lingering 		= models.BooleanField(default=False)
	white 			= models.BooleanField(default=False)
	offwhite 		= models.BooleanField(default=False)
	tan 			= models.BooleanField(default=False)
	frothy 			= models.BooleanField(default=False)
	delicate 		= models.BooleanField(default=False)
	
	def __str__(self):
		return str(self.user) + ' | ' + str(self.bdb_id)

		
class Beer_Attribute_Category(models.Model):
	category		= models.CharField(max_length=50)
	page_order		= models.IntegerField(default=0)
	
	class Meta:
		ordering = ['page_order']
	
	def __str__(self):
		return str(self.category)

		
class Beer_Attribute_Section(models.Model):
	section			= models.CharField(max_length=50)
	category		= models.ForeignKey(Beer_Attribute_Category, on_delete=models.CASCADE)
	
	def __str__(self):
		return str(self.section) + ' | ' + str(self.category)

		
class Beer_Attribute(models.Model):
	attribute 		= models.CharField(max_length=50)
	section			= models.ForeignKey(Beer_Attribute_Section, on_delete=models.CASCADE)		
	class Meta:
		ordering = ['attribute']
	
	def __str__(self):
		return str(self.attribute) + ' | ' + str(self.section)
	
		
class Profile_Sheet(models.Model):
	user	 		= models.ForeignKey(User, on_delete=models.CASCADE)	
	bdb_id			= models.CharField(max_length=20)
	beer_attribute 	= models.ManyToManyField(Beer_Attribute, blank=True)
	
	def __str__(self):
		return str(self.user) + ' | ' + str(self.bdb_id)