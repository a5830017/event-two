from django.conf.urls import url

from . import views

app_name = 'event'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^new_event$', views.new_event, name='new_event'),
    url(r'^(?P<event_id>[0-9]+)/$', views.event_detail, name='event_detail'),
    #url(r'^(?P<event_id>[0-9]+)/(?P<person_id>[0-9]+)$', views.delete_name, name='del_name'),
    url(r'^(?P<event_id>[0-9]+)/delete$', views.delete_name, name='del'),


    url(r'^about$', views.about, name='about'),

]
