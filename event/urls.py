from django.conf.urls import url

from . import views

app_name = 'event'

urlpatterns = [
	
	#ex: /1/
	url(r'^(?P<event_id>[0-9]+)/$', views.one_event, name='one_event'),
	# ex: /
	url(r'^$', views.event, name='event'),
]