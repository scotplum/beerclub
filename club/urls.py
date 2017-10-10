from django.conf.urls import url

from . import views

app_name = 'club'

urlpatterns = [
	
	#ex: /1/
	url(r'^(?P<id>[0-9]+)/$', views.club, name='club'),
	#ex: /1/manage/'
	url(r'^(?P<id>[0-9]+)/manage/$', views.manage, name='manage'),
	#ex: /1/manage/announcement/'
	url(r'^(?P<id>[0-9]+)/manage/announcement/$', views.announcement, name='announcement'),
	#ex: /1/manage/announcement/'
	url(r'^(?P<id>[0-9]+)/manage/about/$', views.about, name='about'),
	#ex: /1/manage/announcement/'
	url(r'^(?P<id>[0-9]+)/manage/membership/$', views.membership, name='membership'),
	#ex: /1/manage/announcement/'
	url(r'^(?P<id>[0-9]+)/manage/event/$', views.event, name='event'),
	#ex: /1/manage/event/addevent/'
	url(r'^(?P<id>[0-9]+)/manage/event/addevent/$', views.addevent, name='addevent'),
	#ex: /add/
	url(r'^add/$', views.add, name='add'),
	#ex: /search/
	url(r'^search/$', views.search, name='search'),
	#ex: /
	url(r'^$', views.index, name='index'),
]