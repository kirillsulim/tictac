from rest_framework.test import APITransactionTestCase
from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class AuthTest(APITransactionTestCase):
  def test_should_create_new_player_and_login(self):
    username = 'johndow'
    password = 'password'

    url = '/rest-auth/registration/'
    data = {
      'username': username,
      'password1': password,
      'password2': password,
    }
    response = self.client.post(url, data, format='json')

    self.assertEquals(response.status_code, status.HTTP_201_CREATED)
    user = User.objects.get(username=username)

    url = '/rest-auth/login/'
    data = {
      'username': 'johndow',
      'password': 'password',
    }
    response = self.client.post(url, data, format='json')

    self.assertEquals(response.status_code, status.HTTP_200_OK)
