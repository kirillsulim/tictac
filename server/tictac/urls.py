from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
  url(r'^accounts/', include('allauth.urls')),
  url(r'^rest-auth/', include('rest_auth.urls')),
  url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
  url(r'^', include('game.urls')),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
