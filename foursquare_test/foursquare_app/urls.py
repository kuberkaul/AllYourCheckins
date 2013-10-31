from django.conf.urls import patterns, url
from foursquare_app import views

urlpatterns = patterns('', url(r'^$', views.index, name = 'index'),
                       url(r'^search/', views.search, name = 'search'),
		       url(r'^mapView', views.mapView, name = 'mapView'),
                       url(r'^imageIndex', views.imageIndex, name = 'imageIndex'),
                       url(r'^friendIndex/', views.friendIndex, name = 'friendIndex'),
                       url(r'^loginError', views.loginError, name = 'loginError'),
                       url(r'^login', views.login, name = 'login'),
		       url(r'^logout',views.logoutuser, name='logout'),
                      )
                   
