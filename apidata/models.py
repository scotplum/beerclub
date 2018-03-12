from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.forms import ModelForm
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
import os

# Create your models here.

class Beer_Category(models.Model):
	name 				= models.CharField(max_length=100)
	category_bdb_id		= models.CharField(max_length=5)
	create_date			= models.DateTimeField(null=True, blank=True)
	
	def __unicode__(self):
		return unicode(self.name) + ' | ' + unicode(self.id)
		
class Beer_Style(models.Model):
	style_bdb_id		= models.CharField(max_length=5)
	name				= models.CharField(max_length=100)
	description		 	= models.CharField(max_length=1500, null=True, blank=True)
	category			= models.ForeignKey(Beer_Category, on_delete=models.CASCADE) 
	ibuMin				= models.CharField(max_length=20, null=True, blank=True)
	ibuMax				= models.CharField(max_length=20, null=True, blank=True)
	abvMin				= models.CharField(max_length=20, null=True, blank=True)
	abvMax				= models.CharField(max_length=20, null=True, blank=True)
	srmMin				= models.CharField(max_length=20, null=True, blank=True)
	srmMax				= models.CharField(max_length=20, null=True, blank=True)
	ogMin				= models.CharField(max_length=20, null=True, blank=True)
	ogMax				= models.CharField(max_length=20, null=True, blank=True)
	fgMin				= models.CharField(max_length=20, null=True, blank=True)
	fgMax				= models.CharField(max_length=20, null=True, blank=True)
	create_date			= models.DateTimeField(null=True, blank=True)
	update_date			= models.DateTimeField(null=True, blank=True)
	
	def __unicode__(self):
		return unicode(self.name) + ' | ' + unicode(self.id)