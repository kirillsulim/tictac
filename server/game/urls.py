from django.conf.urls import url

from .views import *


urlpatterns = [
  url(r'^players$', PlayerList.as_view(), name='players'),
  url(r'^invites$', InviteList.as_view(), name='invite-list'),
  url(r'^invite/(?P<pk>\d+)$', InviteDetails.as_view(), name='invite'),
]