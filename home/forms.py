from django import forms 
from django.forms import ModelForm, inlineformset_factory
from models import Favorite_Beers, Wanted_Beers, Profile_Sheet, Beer_Attribute
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField

from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset 
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions 
from crispy_forms.bootstrap import TabHolder, Tab 

# Adding Favorite Beers 
class findbeerForm(forms.Form): 
    beer = forms.CharField(label='', max_length=150) 
    def __init__(self, *args, **kwargs): 
        self.helper = FormHelper() 
        self.helper.form_class = 'form-inline' 
        self.helper.form_id = 'findbeerForm' 
        self.helper.form_method = 'post' 
        self.helper.form_action = 'findbeer/' 
         
        self.helper.add_input(Submit('submit', 'Beer Me')) 
        super(findbeerForm, self).__init__(*args, **kwargs)

class CustomSelectMultiple(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" %(obj.attribute)

class ProfileSheetForm(forms.ModelForm):
    beer_attribute = CustomSelectMultiple(widget=forms.CheckboxSelectMultiple, queryset=Beer_Attribute.objects.all())
    class Meta:
        model = Profile_Sheet
        widgets = {"beer_attribute":CheckboxSelectMultiple(),}
        exclude = ('user','bdb_id',)
	
class SignupForm(forms.Form):
	first_name = forms.CharField(max_length=30, label='First Name', widget=forms.TextInput(attrs={'placeholder':'First Name'}))
	last_name = forms.CharField(max_length=30, label='Last Name', widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
	
	def signup(self, request, user):
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.save()