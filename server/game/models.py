from django.db import models
from django.contrib.auth.models import User


class GameException(Exception):
  pass


class NotAllowedGame(GameException):
  pass


class NotAllowedPlayer(GameException):
  pass


class NotAllowedMove(GameException):
  pass


class NotYourTurn(GameException):
  pass


class Game(models.Model):
  STATES = (
    ('XP', 'X pending'),
    ('OP', 'O pending'),
    ('XW', 'X won'),
    ('OW', 'O won'),
  )

  x_player = models.ForeignKey(User, related_name='x_player')
  o_player = models.ForeignKey(User, related_name='o_player')
  state = models.CharField(max_length=2, choices=STATES, default=STATES[0][0])
  moves = models.ManyToManyField('game.Move')

  def make_move(self, move):
    if self != move.game:
      raise NotAllowedGame()

    is_x = move.player == self.x_player
    is_o = move.player == self.o_player

    if not is_x and not is_o:
      raise NotAllowedPlayer()

    if (self.state == 'XP' and is_o) or (self.state == 'OP' and is_x):
      raise NotYourTurn()

    for m in self.moves:
      if m.code == move.code:
        raise NotAllowedMove()


class Move(models.Model):
  CODES = (
    ('A1', 'A1'),
    ('A2', 'A2'),
    ('A3', 'A3'),
    ('B1', 'B1'),
    ('B2', 'B2'),
    ('B3', 'B3'),
    ('C1', 'C1'),
    ('C2', 'C2'),
    ('C3', 'C3'),
  )

  player = models.ForeignKey(User)
  game = models.ForeignKey('game.Game')
  order = models.IntegerField()
  code = models.CharField(max_length=2, choices=CODES)


