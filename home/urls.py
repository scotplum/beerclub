from django.conf.urls import url
from . import views
from django.conf import settings

app_name = 'home'

urlpatterns = [
	#ex: /findbeer/
	url(r'^findbeer/$', views.findbeer, name='findbeer'),
	#ex: /profile/
	url(r'^profile/$', views.profile, name='profile'),
	#ex: /findbeer/ID9EJ3/profilesheet/
	url(r'^findbeer/(?P<bdb_id>[A-Za-z0-9]+)/profilesheet/$', views.profilesheet, name='profilesheet'),
	#ex: /findbeer/ID9EJ3/event/
	url(r'^findbeer/(?P<bdb_id>[A-Za-z0-9]+)/event/$', views.beerevent, name='beerevent'),
	#ex: /findbeer/ID9EJ3/10/
	url(r'^findbeer/(?P<bdb_id>[A-Za-z0-9]+)/(?P<club_id>[0-9]+)/$', views.detail, name='detail'),
	#ex: /brewery/TqC06u/
	url(r'^brewery/(?P<brew_id>[A-Za-z0-9]+)/$', views.brewery, name='brewery'),
	#ex: /ratings/
	url(r'^ratings/$', views.ratings, name='ratings'),
	#ex: /breweryscores/
	url(r'^breweryscores/$', views.breweryscores, name='breweryscores'),
	#ex: /notes/
	url(r'^notes/$', views.notes, name='notes'),
	#ex: /notes/30/1/share/
	url(r'^notes/(?P<id>[A-Za-z0-9]+)/(?P<social_id>[0-9]+)/share/$', views.share, name='noteshare'),
	#ex: /notes/ID9EJ3/
	url(r'^notes/(?P<id>[A-Za-z0-9]+)/$', views.noteedit, name='noteedit'),
	#ex: /brewerynotes/
	url(r'^brewerynotes/$', views.brewerynotes, name='brewerynotes'),
	#ex: /brewerynotes/ID9EJ3/1/share/
	url(r'^brewerynotes/(?P<id>[A-Za-z0-9]+)/(?P<social_id>[0-9]+)/share/$', views.share, name='brewerynoteshare'),
	#ex: /brewerynotes/ID9EJ3/
	url(r'^brewerynotes/(?P<id>[A-Za-z0-9]+)/$', views.brewerynoteedit, name='brewerynoteedit'),
	#ex: /tasters/id/
	url(r'^tasters/(?P<id>[0-9]+)/$', views.taster, name='taster'),
	#ex: /tasters/
	url(r'^tasters/', views.tasters, name='tasters'),
	#ex: /ID9EJ3/amber-by-abita/addbeerimage/
	url(r'^(?P<bdb_id>[A-Za-z0-9]+)/(?P<slug>[-\w\d]+)/addbeerimage/$', views.addbeerimage, name='addbeerimage'),	
	#ex: /ID9EJ3/amber-by-abita/editbeerimage/1/
	url(r'^(?P<bdb_id>[A-Za-z0-9]+)/(?P<slug>[-\w\d]+)/editbeerimage/(?P<id>[0-9]+)/$', views.editbeerimage, name='editbeerimage'),
	#ex: /ID9EJ3/amber-by-abita/
	url(r'^(?P<bdb_id>[A-Za-z0-9]+)/(?P<slug>[-\w\d]+)/$', views.beer, name='beer'),
	#ex: /ID9EJ3/amber-by-abita/share/
	url(r'^(?P<id>[A-Za-z0-9]+)/([-\w\d]+)/(?P<social_id>[0-9]+)/share/$', views.share, name='beershare'),
	# ex: /
	url(r'^$', views.index, name='home'),
]