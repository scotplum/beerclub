from django.conf.urls import url

from . import views

app_name = 'home'

urlpatterns = [
	# ex: /
	url(r'^', views.index, name='home'),
]