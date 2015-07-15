from rest_framework.test import APITransactionTestCase, APITestCase
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
    move.for_game = game
    move.player = player
    move.code = code
    return move

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

  def test_should_raise_not_allowed_move(self):
    game = self.create_game()
    move1 = self.create_move(game, self.x_player, 'A1')
    game.make_move(move1)
    move2 = self.create_move(game, self.o_player, 'A1')

    self.assertRaises(NotAllowedMove, game.make_move, move2)

  def test_mimic_game(self):
    game = self.create_game()
    move = self.create_move(game, self.x_player, 'A1')
    game.make_move(move)
    self.assertEquals(game.state, 'OP')

    move = self.create_move(game, self.o_player, 'A2')
    game.make_move(move)
    self.assertEquals(game.state, 'XP')

    move = self.create_move(game, self.x_player, 'B1')
    game.make_move(move)
    self.assertEquals(game.state, 'OP')

    move = self.create_move(game, self.o_player, 'B2')
    game.make_move(move)
    self.assertEquals(game.state, 'XP')

    move = self.create_move(game, self.x_player, 'C1')
    game.make_move(move)
    self.assertEquals(game.state, 'XW')

  def test_should_not_accept_if_finished(self):
    game = self.create_game()
    move = self.create_move(game, self.x_player, 'A1')
    game.make_move(move)

    move = self.create_move(game, self.o_player, 'A2')
    game.make_move(move)

    move = self.create_move(game, self.x_player, 'B1')
    game.make_move(move)

    move = self.create_move(game, self.o_player, 'B2')
    game.make_move(move)

    move = self.create_move(game, self.x_player, 'C1')
    game.make_move(move)

    move = self.create_move(game, self.o_player, 'C2')

    self.assertRaises(NotYourTurn, game.make_move, move)



class GameCounterTest(APITestCase):
  def test_should_mark_no_win(self):
    counter = GameCounter()
    counter.add_code('A2')
    counter.add_code('C1')
    counter.add_code('B1')
    self.assertFalse(counter.win())

  def test_should_mark_letters_win(self):
    counter = GameCounter()
    counter.add_code('A1')
    counter.add_code('A2')
    counter.add_code('A3')
    self.assertTrue(counter.win())

  def test_should_mark_nums_win(self):
    counter = GameCounter()
    counter.add_code('B2')
    counter.add_code('C2')
    counter.add_code('A2')
    self.assertTrue(counter.win())

  def test_should_mark_a1c3_win(self):
    counter = GameCounter()
    counter.add_code('B2')
    counter.add_code('A1')
    counter.add_code('C3')
    self.assertTrue(counter.win())

  def test_should_mark_a3c1_win(self):
    counter = GameCounter()
    counter.add_code('B2')
    counter.add_code('A3')
    counter.add_code('C1')
    self.assertTrue(counter.win())








