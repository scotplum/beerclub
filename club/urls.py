from django.conf.urls import url

from . import views

app_name = 'club'

urlpatterns = [
	
	#ex: /1/
	url(r'^(?P<id>[0-9]+)/$', views.club, name='club'),
	# ex: /
	url(r'^$', views.index, name='index'),
]