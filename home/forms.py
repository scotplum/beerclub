from django import forms 
from django.forms import ModelForm 
from models import Favorite_Beers, Wanted_Beers

from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset 
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions 
from crispy_forms.bootstrap import TabHolder, Tab 

# Adding Favorite Beers 
class findbeerForm(forms.Form): 
    beer = forms.CharField(label='', max_length=150) 
    def __init__(self, *args, **kwargs): 
        self.helper = FormHelper() 
        self.helper.form_id = 'findbeerForm' 
        self.helper.form_class = 'form-horizontal' 
        self.helper.form_method = 'post' 
        self.helper.form_action = 'findbeer/' 
         
        self.helper.add_input(Submit('submit', 'Beer Me')) 
        super(findbeerForm, self).__init__(*args, **kwargs)
		
#class beerForm(forms.Form):
#	user 			= user_object
#	beer_name		= data['name']
#	beer_company 	= brewery['name']
#	beer_category 	= style['name']
#	date_added 	= timezone.now()
#	is_active 		= 
#	bdb_id			= bdb_id