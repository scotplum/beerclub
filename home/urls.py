from django.conf.urls import url

from . import views

app_name = 'home'

urlpatterns = [
	#ex: /findbeer/
	url(r'^findbeer/$', views.findbeer, name='findbeer'),
	#ex: /profile/
	url(r'^profile/$', views.profile, name='profile'),
	#ex: /findbeer/ID9EJ3/
	url(r'^findbeer/(?P<bdb_id>[A-Za-z0-9]+)/$', views.beer, name='beer'),
	#ex: /findbeer/ID9EJ3/profilesheet/
	url(r'^findbeer/(?P<bdb_id>[A-Za-z0-9]+)/profilesheet/$', views.profilesheet, name='profilesheet'),
	#ex: /findbeer/ID9EJ3/event/
	url(r'^findbeer/(?P<bdb_id>[A-Za-z0-9]+)/event/$', views.beerevent, name='beerevent'),
	#ex: /ratings/
	url(r'^ratings/$', views.ratings, name='ratings'),
	#ex: /notes/
	url(r'^notes/$', views.notes, name='notes'),
	#ex: /notes/ID9EJ3/
	url(r'^notes/(?P<id>[A-Za-z0-9]+)/', views.noteedit, name='noteedit'),
	#ex: /tasters/id/
	url(r'^tasters/(?P<id>[0-9]+)/$', views.taster, name='taster'),
	#ex: /tasters/
	url(r'^tasters/', views.tasters, name='tasters'),
	# ex: /
	url(r'^$', views.index, name='home'),
]