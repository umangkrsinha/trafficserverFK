from django.conf.urls import url
import views

app_name = 'junction'
urlpatterns=[
	url(r'^upload/$', views.upload, name='upload'),
	url(r'^$', views.index, name='index'),
]
