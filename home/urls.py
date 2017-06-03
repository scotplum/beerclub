from django.conf.urls import url

from . import views

app_name = 'home'

urlpatterns = [
	#ex: /findbeer/
	url(r'^findbeer/$', views.findbeer, name='findbeer'),
	#ex: /findbeer/ID9EJ3/
	url(r'^findbeer/(?P<bdb_id>[A-Za-z0-9]+)/$', views.beer, name='beer'),
	# ex: /
	url(r'^$', views.index, name='home'),
]