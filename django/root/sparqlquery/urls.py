from django.conf.urls import patterns, url

from sparqlquery import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<person_id>\d+)/page/$', views.person_page, name='person'),
    url(r'^(?P<person_id>\d+)/test/$', views.test_page, name='person'),
    url(r'^(?P<person_id>\d+)/(?P<content_type>\w+)/$', views.person, name='person'),
    url(r'^(?P<person_id>\d+)/$', views.person_page, name='person'),
)
