from rest_framework.test import APITransactionTestCase
from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from game.models import*


class GameTest(APITransactionTestCase):
  def setUp(self):
    self.u1 = User.objects.create_user(username='u1', password='u1')
    self.u2 = User.objects.create_user(username='u2', password='u2')

  def test_should_access_game_list(self):
    Game.objects.create(x_player=self.u1, o_player=self.u2, state='XP')
    Game.objects.create(x_player=self.u1, o_player=self.u2, state='XP')

    url = reverse('game-list')

    self.client.login(username='u1', password='u1')
    response = self.client.get(url)

    self.assertEquals(response.status_code, status.HTTP_200_OK)
    self.assertEquals(len(response.data), 2)
    self.assertEquals(response.data[0]['state'], 'XP')
    self.assertEquals(response.data[1]['state'], 'XP')

  def test_should_get_game_info(self):
    g = Game.objects.create(x_player=self.u1, o_player=self.u2, state='XP')

    url = reverse('game', args=[g.pk])

    self.client.login(username='u1', password='u1')
    response = self.client.get(url)

    self.assertEquals(response.status_code, status.HTTP_200_OK)
    self.assertEquals(response.data['state'], 'XP')


class MakeMoveTest(APITransactionTestCase):
  def setUp(self):
    self.u1 = User.objects.create_user(username='u1', password='u1')
    self.u2 = User.objects.create_user(username='u2', password='u2')

  def test_should_allow_move(self):
    game = Game.objects.create(x_player=self.u1, o_player=self.u2, state='XP')

    self.client.login(username='u1', password='u1')

    url = reverse('move')
    response = self.client.post(url, data={'for_game': game.pk, 'code': 'A1'}, format='json')

    game = Game.objects.get(pk=game.pk)

    self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)
    self.assertEquals(response.data['state'], 'OP')

    self.assertEquals(game.moves.count(), 1)
    self.assertEquals(game.state, 'OP')

  def test_should_not_allow_wrong_turn(self):
    game = Game.objects.create(x_player=self.u1, o_player=self.u2, state='XP')

    self.client.login(username='u1', password='u1')

    url = reverse('move')
    response = self.client.post(url, data={'for_game': game.pk, 'code': 'A1'}, format='json')
    response = self.client.post(url, data={'for_game': game.pk, 'code': 'A2'}, format='json')

    self.assertEquals(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
    self.assertEquals(response.data['error'], 'NotYourTurn')

  def test_should_not_allow_wrong_moves(self):
    game = Game.objects.create(x_player=self.u1, o_player=self.u2, state='XP')
    url = reverse('move')

    self.client.login(username='u1', password='u1')
    response = self.client.post(url, data={'for_game': game.pk, 'code': 'A1'}, format='json')

    self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)
    self.assertEquals(response.data['state'], 'OP')

    self.client.login(username='u2', password='u2')
    response = self.client.post(url, data={'for_game': game.pk, 'code': 'A1'}, format='json')

    self.assertEquals(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
    self.assertEquals(response.data['error'], 'NotAllowedMove')

  def test_mimic_game(self):
    game = Game.objects.create(x_player=self.u1, o_player=self.u2, state='XP')
    url = reverse('move')

    self.client.login(username='u1', password='u1')
    response = self.client.post(url, data={'for_game': game.pk, 'code': 'A1'}, format='json')

    self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)
    self.assertEquals(response.data['state'], 'OP')

    self.client.login(username='u2', password='u2')
    response = self.client.post(url, data={'for_game': game.pk, 'code': 'A2'}, format='json')

    self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)
    self.assertEquals(response.data['state'], 'XP')

    self.client.login(username='u1', password='u1')
    response = self.client.post(url, data={'for_game': game.pk, 'code': 'B1'}, format='json')

    self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)
    self.assertEquals(response.data['state'], 'OP')

    self.client.login(username='u2', password='u2')
    response = self.client.post(url, data={'for_game': game.pk, 'code': 'B2'}, format='json')

    self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)
    self.assertEquals(response.data['state'], 'XP')

    self.client.login(username='u1', password='u1')
    response = self.client.post(url, data={'for_game': game.pk, 'code': 'C1'}, format='json')

    self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)
    self.assertEquals(response.data['state'], 'XW')












