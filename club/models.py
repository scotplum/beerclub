from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Club(models.Model): 
    name	  		= models.CharField(max_length=100) 
    date_added   	= models.DateTimeField(auto_now_add=True) 
    is_active   	= models.BooleanField(default=True) 

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

	def __str__(self):
		return str(self.user) + ' | ' + str(self.club)