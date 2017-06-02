from django.conf.urls import url

from . import views

app_name = 'home'

urlpatterns = [
	#ex: /findbeer/
	url(r'^findbeer/', views.findbeer, name='findbeer'),
	# ex: /
	url(r'^', views.index, name='home'),
]