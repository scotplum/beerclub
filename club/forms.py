from django import forms 
from django.forms import ModelForm, inlineformset_factory
from models import Club, Club_Announcement, Club_User
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField

from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset 
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions 
from crispy_forms.bootstrap import TabHolder, Tab 

class ClubForm(forms.ModelForm):
	established = forms.DateField(widget=forms.DateInput(format = '%m/%d/%Y'),input_formats=('%m/%d/%Y',))
	
	class Meta:
		model = Club
		exclude = ('date_added',)
	
class ClubAnnouncementForm(forms.ModelForm):	
	class Meta:
		model = Club_Announcement
		exclude = ('expiration_date',)
		
class ClubMembershipForm(forms.ModelForm):
	class Meta:
		model = Club_User
		exclude = ('club',)