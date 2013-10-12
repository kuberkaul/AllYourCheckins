from django.conf.urls import patterns, url

from foursquare_app import views

urlpatterns = patterns('', url(r'^$', views.index, name = 'index'),
                       url(r'^welcome/', views.welcome, name = 'welcome') )
