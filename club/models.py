from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from event.models import Event
from localflavor.us.models import USStateField
import datetime

# Create your models here.

class Club(models.Model): 
    name	  		= models.CharField(max_length=100) 
    date_added   	= models.DateTimeField(auto_now_add=True) 
    is_active   	= models.BooleanField(default=True) 
    city			= models.CharField(max_length=100)
    state			= USStateField(null=True, blank=True)
    is_public		= models.BooleanField(default=False)
    established		= models.DateField(default=datetime.date.today)
    annual_fee		= models.DecimalField(max_digits=6, decimal_places=2)
    bio				= models.TextField(max_length=1000)

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
	is_active 		= models.BooleanField(default=False)
	is_admin		= models.BooleanField(default=False)
	
	class Meta:
		ordering = ['user__last_name']

	def __str__(self):
		return str(self.user) + ' | ' + str(self.club)
		
class Club_Announcement(models.Model):
	club			= models.ForeignKey(Club, on_delete=models.CASCADE)
	announcement	= models.TextField(max_length=1000)
	is_active		= models.BooleanField(default=True)
	expiration_date	= models.DateTimeField(null=True, blank=True)
	date_added		= models.DateField(default=datetime.date.today, blank=True)
	
	class Meta:
		ordering = ['-date_added']
	
	def __str__(self):
		return str(self.club) + ' | ' + str(self.announcement)
	
class Club_Event(models.Model):
	club 			= models.ForeignKey(Club, on_delete=models.CASCADE)
	event			= models.ForeignKey(Event, on_delete=models.CASCADE)
	
	def __str__(self):
		return str(self.club) + ' | ' + str(self.event) 

STATUS_CHOICES = (
	('accepted', 'ACCEPTED'),
	('rejected', 'REJECTED'),
	('pending', 'PENDING'),
)
		
class Club_Application(models.Model):
	club			= models.ForeignKey(Club, on_delete=models.CASCADE)
	user			= models.ForeignKey(User, on_delete=models.CASCADE)
	date_applied	= models.DateTimeField(auto_now_add=True)
	status			= models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending')
	date_completed	= models.DateTimeField(null=True, blank=True)
	
	def __str__(self):
		return str(self.club) + ' | ' + str(self.user) + ' | ' + self.status