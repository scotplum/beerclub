from django.conf.urls import url

from . import views

app_name = 'home'

urlpatterns = [
	#ex: /findbeer/
	url(r'^findbeer/$', views.findbeer, name='findbeer'),
	#ex: /findbeer/ID9EJ3/
	url(r'^findbeer/(?P<bdb_id>[A-Za-z0-9]+)/$', views.beer, name='beer'),
	#ex: /findbeer/ID9EJ3/event/
	url(r'^findbeer/(?P<bdb_id>[A-Za-z0-9]+)/event/$', views.beerevent, name='beerevent'),
	#ex: /tasters/id/
	url(r'^tasters/(?P<id>[0-8]+)/$', views.taster, name='taster'),
	#ex: /tasters/
	url(r'^tasters/', views.tasters, name='tasters'),
	# ex: /
	url(r'^$', views.index, name='home'),
]