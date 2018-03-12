from django import forms 
from django.forms import ModelForm, inlineformset_factory
from models import Favorite_Beers, Wanted_Beers, Profile_Sheet, Beer_Attribute, Beer_User_Image
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField
from django.contrib.auth.models import User 
from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset, ButtonHolder
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
        self.helper.form_action = '/home/findbeer/' 
         
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
	
		
class ProfileForm(forms.ModelForm):
	
	email = forms.CharField(max_length=75, required=True)
	
	class Meta:
		model = User
		fields = ('last_name', 'first_name',  'email',)
		
class BeerImageForm(forms.ModelForm):
	class Meta:
		model = Beer_User_Image
		fields = ('description', 'beer_image')
		
class BeerImageEditForm(forms.ModelForm):
	class Meta:
		model = Beer_User_Image
		fields = ('description', 'is_active')
		
class AddBeerForm(forms.Form):
    beer_name = forms.CharField(
        label = "Name of Beer",
        max_length = 120,
        required = True,
    )
    beer_style = forms.ChoiceField(
        label = "Select Beer Style",
        choices = ((2, "Test"), (1, "Yes"), (0, "No")),
        initial = '2',
        required = True,
    )
    beer_description = forms.CharField(
        label = "Description",
        max_length = 500,
        required = False,
        widget=forms.Textarea
    )
    def __init__(self, *args, **kwargs): 
        self.helper = FormHelper() 
        self.helper.form_class = 'homebeer'
        self.helper.form_id = 'AddBeerForm' 
        self.helper.form_method = 'post' 
        self.helper.form_action = '' 
        self.helper.layout = Layout(
            Fieldset(
			'',
			'beer_name',
			'beer_style',
			'beer_description',
			),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )
        self.helper.label_class = 'crispy-label'
        self.helper.field_class = 'content-base crispy-field'

        super(AddBeerForm, self).__init__(*args, **kwargs)