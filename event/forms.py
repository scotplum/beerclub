from django import forms 
from django.forms import ModelForm, inlineformset_factory
from models import Event, Event_Address
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField
from club.models import Club

from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset 
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions 
from crispy_forms.bootstrap import TabHolder, Tab 

class EventForm(forms.ModelForm):
	event_date = forms.DateTimeField(widget=forms.DateTimeInput(format = '%m/%d/%Y %H:%M'),input_formats=('%m/%d/%Y %H:%M',))

	def __init__(self, club=None, **kwargs):
		super(EventForm, self).__init__(**kwargs)
		self.fields['address'].queryset = Event_Address.objects.filter(club=club)
	class Meta:
		model = Event
		exclude = ('date_created',)
		
class EventEditForm(forms.ModelForm):
	event_date = forms.DateTimeField(widget=forms.DateTimeInput(format = '%m/%d/%Y %H:%M'),input_formats=('%m/%d/%Y %H:%M',))

	class Meta:
		model = Event
		exclude = ('date_created',)
		
class EventAddressForm(forms.ModelForm):
	class Meta:
		model = Event_Address
		exclude = ('club', 'google_maps',)
		
class EventAddressEditForm(forms.ModelForm):
	class Meta:
		model = Event_Address
		exclude = ('club', 'google_maps',)