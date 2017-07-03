from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.translation import ugettext as _

# Create your models here.

class Event_Address(models.Model):
    description 	= models.CharField(_("description"),max_length=128)
    address_1 		= models.CharField(_("address"), max_length=128)
    address_2 		= models.CharField(_("address cont'd"), max_length=128, blank=True)
    city 			= models.CharField(_("city"), max_length=64, default="Oklahoma City")
    state 			= models.CharField(_("state"), max_length=2,default="OK")
    zip_code 		= models.CharField(_("zip code"), max_length=5, default="73142")
    google_maps		= models.URLField(_("goolge maps"), max_length=200)
	
    def __str__(self):
		return self.description

class Event(models.Model):
	event_name			= models.CharField(max_length=50)
	date_created 		= models.DateTimeField(auto_now_add=True)
	event_date			= models.DateTimeField(blank=True)
	is_active			= models.BooleanField(default=True)
	address				= models.ForeignKey(Event_Address, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.event_name + " | Is Active: " + str(self.is_active)
	
class Event_Beer(models.Model):
	user	 		= models.ForeignKey(User, on_delete=models.CASCADE)
	event			= models.ForeignKey(Event, on_delete=models.CASCADE)
	beer_company 	= models.CharField(max_length=100)
	beer_name		= models.CharField(max_length=500)
	beer_category	= models.CharField(max_length=100)
	date_added	 	= models.DateTimeField(auto_now_add=True)
	is_active 		= models.BooleanField(default=True)
	bdb_id          = models.CharField(max_length=20)
	
	def __str__(self):
		return self.beer_name + ' | ' + str(self.user) + ' | ' + str(self.event)

class Event_Attend(models.Model):
	user	 		= models.ForeignKey(User, on_delete=models.CASCADE)
	event			= models.ForeignKey(Event, on_delete=models.CASCADE)
	will_attend		= models.BooleanField(default=True)
	date_added	 	= models.DateTimeField(auto_now_add=True)
	
class Event_Note(models.Model):
	user	 		= models.ForeignKey(User, on_delete=models.CASCADE)
	event			= models.ForeignKey(Event, on_delete=models.CASCADE)
	is_active		= models.BooleanField(default=True)
	date_added		= models.DateTimeField(auto_now_add=True)
	note			= models.CharField(max_length=500)
	
	def __str__self(self):
		return self.user + ' | ' + self.event + ' | ' + self.note