from django.conf.urls import include, url

from event import views
from django.contrib import admin

urlpatterns = [
    url(r'^', include('event.urls')),
    url(r'^admin/', include(admin.site.urls)),
]