from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from event.models import Event
from localflavor.us.models import USStateField

# Create your models here.

class Club(models.Model): 
    name	  		= models.CharField(max_length=100) 
    date_added   	= models.DateTimeField(auto_now_add=True) 
    is_active   	= models.BooleanField(default=True) 
    city			= models.CharField(max_length=100)
    state			= USStateField(null=True, blank=True)
    is_public		= models.BooleanField(default=False)

    def __str__(self):
		return self.name

class Club_Admin(models.Model):
	user			= models.ForeignKey(User, on_delete=models.CASCADE)
	club			= models.ForeignKey(Club, on_delete=models.CASCADE)
	date_added		= models.DateTimeField(auto_now_add=True) 
	is_active		= models.BooleanField(default=True) 
	
	def __str__(self):
		return str(self.user) + ' | ' + str(self.club)

class Club_User(models.Model):
	user	 		= models.ForeignKey(User, on_delete=models.CASCADE)
	club			= models.ForeignKey(Club, on_delete=models.CASCADE)
	is_active 		= models.BooleanField(default=True)

	def __str__(self):
		return str(self.user) + ' | ' + str(self.club)
		
class Club_Announcement(models.Model):
	club			= models.ForeignKey(Club, on_delete=models.CASCADE)
	announcement	= models.CharField(max_length=1000)
	is_active		= models.BooleanField(default=True)
	expiration_date	= models.DateTimeField(auto_now_add=False)
	date_added		= models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return str(self.club) + ' | ' + str(self.announcement)
	
class Club_Event(models.Model):
	club 			= models.ForeignKey(Club, on_delete=models.CASCADE)
	event			= models.ForeignKey(Event, on_delete=models.CASCADE)
	
	def __str__(self):
		return str(self.club) + ' | ' + str(self.event) 