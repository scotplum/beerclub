from django.conf.urls import url

from . import views

app_name = 'event'

urlpatterns = [
	# ex: /
	url(r'^$', views.event, name='event'),
]