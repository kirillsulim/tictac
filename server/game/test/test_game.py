from rest_framework.test import APITransactionTestCase
from django.contrib.auth.models import User

from game.models import *


class GameTest(APITransactionTestCase):
  def setUp(self):
    self.x_player = User.objects.create(username='ux', password='uxp')
    self.o_player = User.objects.create(username='uo', password='uop')
    self.wrong_player = User.objects.create(username='wrong', password='wrong')

  def create_game(self):
    game = Game()
    game.x_player = self.x_player
    game.o_player = self.o_player
    game.save()
    return game

  def create_move(self, game, player=None, code='A1'):
    if not player:
      player = self.x_player

    move = Move()
    move.game = game
    move.player = player
    move.code = code
    return move

  def test_should_allow_do_move(self):
    game = self.create_game()
    move = self.create_move(game)

  def test_should_raise_wrong_player(self):
    game = self.create_game()
    move = self.create_move(game, self.wrong_player)
    self.assertRaises(NotAllowedPlayer, game.make_move, move)

  def test_should_raise_not_your_turn(self):
    game = self.create_game()
    move = self.create_move(game, self.o_player)
    self.assertRaises(NotYourTurn, game.make_move, move)

  def test_should_raise_not_allowed_game(self):
    game = self.create_game()
    game2 = self.create_game()
    move = self.create_move(game2)
    self.assertRaises(NotAllowedGame, game.make_move, move)











