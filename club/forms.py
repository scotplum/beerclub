from django import forms 
from django.forms import ModelForm, inlineformset_factory
from models import Club, Club_Announcement, Club_User
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField
from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset 
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions 
from crispy_forms.bootstrap import TabHolder, Tab 
from localflavor.us.us_states import STATE_CHOICES

class ClubForm(forms.ModelForm):
	established = forms.DateField(widget=forms.DateInput(format = '%m/%d/%Y'),input_formats=('%m/%d/%Y',))
	YOUR_STATE_CHOICES = list(STATE_CHOICES)
	YOUR_STATE_CHOICES.insert(0, ('ZZ', 'Website Only'))
	YOUR_STATE_CHOICES.insert(0, ('', '---------'))
	state		= forms.ChoiceField(choices = YOUR_STATE_CHOICES, required=True)
	
	class Meta:
		model = Club
		exclude = ('date_added', 'disp_members', 'display_member_vote', 'display_wanted_beer',)
	
class ClubAnnouncementForm(forms.ModelForm):	
	date_added = forms.DateField(widget=forms.DateInput(format = '%m/%d/%Y'),input_formats=('%m/%d/%Y',))
	
	class Meta:
		model = Club_Announcement
		exclude = ('expiration_date', 'club',)
		
class ClubMembershipForm(forms.ModelForm):
	class Meta:
		model = Club_User
		exclude = ('club',)
		
class ClubDisplayForm(forms.ModelForm):
	
	class Meta:
		model = Club
		fields = ('disp_members', 'display_member_vote', 'display_wanted_beer', 'auto_approve',)