from rest_framework.test import APITransactionTestCase
from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from game.models import*


class PlayerListTest(APITransactionTestCase):
  def test_should_return_players_list(self):
    User.objects.create_user(username='u1')
    User.objects.create_user(username='u2')
    User.objects.create_user(username='current', password='current')

    self.client.login(username='current', password='current')

    url = reverse('players')
    response = self.client.get(url)

    self.assertEquals(response.status_code, status.HTTP_200_OK)

    u1 = response.data[0]['username']
    u2 = response.data[1]['username']
    self.assertEquals(u1, 'u1')
    self.assertEquals(u2, 'u2')

class InviteGameTest(APITransactionTestCase):
  def test_should_invite_player(self):
    u1 = User.objects.create_user(username='u1', password='u1')
    u2 = User.objects.create_user(username='u2', password='u2')

    url = reverse('invite-list')

    self.client.login(username='u1', password='u1')
    response = self.client.post(url, data={
      'to_player': u2.pk,
      'from_player': u1.pk,
      'state': 'I',
    }, format='json')

    self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    invite = Invite.objects.get(pk=response.data['pk'])
    self.assertEquals(invite.from_player, u1)
    self.assertEquals(invite.to_player, u2)
    self.assertEquals(invite.state, 'I')

  def test_should_accept_invite(self):
    u1 = User.objects.create_user(username='u1', password='u1')
    u2 = User.objects.create_user(username='u2', password='u2')
    invite = Invite.objects.create(from_player=u1, to_player=u2, state='I')

    url = reverse('invite', args=[invite.pk])

    self.client.login(username='u2', password='u2')
    response = self.client.put(url, data={'state': 'A'}, format='json')

    self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)

    invite = Invite.objects.get(pk=invite.pk)
    self.assertEquals(invite.state, 'A')

  def test_should_delete_invite(self):
    u1 = User.objects.create_user(username='u1', password='u1')
    u2 = User.objects.create_user(username='u2', password='u2')
    invite = Invite.objects.create(from_player=u1, to_player=u2, state='I')

    url = reverse('invite', args=[invite.pk])

    self.client.login(username='u2', password='u2')
    response = self.client.delete(url)

    self.assertEquals(response.status_code, status.HTTP_200_OK)

    invite = Invite.objects.get(pk=invite.pk)
    self.assertEquals(invite.state, 'D')

  def test_should_form_list_with_active_invites(self):
    u1 = User.objects.create_user(username='u1', password='u1')
    u2 = User.objects.create_user(username='u2', password='u2')
    invite = Invite.objects.create(from_player=u1, to_player=u2, state='I')
    Invite.objects.create(from_player=u1, to_player=u2, state='A')
    Invite.objects.create(from_player=u1, to_player=u2, state='D')

    self.client.login(username='u2', password='u2')
    url = reverse('invite-list')
    response = self.client.get(url)

    self.assertEquals(response.status_code, status.HTTP_200_OK)

    self.assertEquals(len(response.data), 1)
    invite = Invite.objects.get(pk=response.data[0]['pk'])
    self.assertEquals(invite.from_player, u1)
    self.assertEquals(invite.to_player, u2)
    self.assertEquals(invite.state, 'I')






