from django.conf.urls import url

from . import views

app_name = 'apidata'

urlpatterns = [
	
	#ex: /apidata/
	url(r'^$', views.update, name='update'),
]