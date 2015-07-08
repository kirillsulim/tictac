from django.db import models
from django.contrib.auth.models import User


# TODO: REFACTOR! Game logic should be separated from models

class Invite(models.Model):
  STATES = (
    ('I', 'Invited'),
    ('A', 'Accepted'),
    ('D', 'Declined'),
  )
  from_player = models.ForeignKey(User, related_name='from_player')
  to_player = models.ForeignKey(User, related_name='to_player')
  state = models.CharField(max_length=1, choices=STATES)


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


class GameCounter:
  a1c3_diagonal_codes = ['A1', 'B2', 'C3']
  a3c1_diagonal_codes = ['A3', 'B2', 'C1']

  def __init__(self):
    self.nums_letters = {
      '1': 0,
      '2': 0,
      '3': 0,
      'A': 0,
      'B': 0,
      'C': 0,
    }
    self.a1c3_diagonal = 0
    self.a3c1_diagonal = 0

  def add_code(self, code):
    letter = code[0]
    number = code[1]

    self.nums_letters[letter] += 1
    self.nums_letters[number] += 1

    if code in self.a1c3_diagonal_codes:
      self.a1c3_diagonal += 1
    if code in self.a3c1_diagonal_codes:
      self.a3c1_diagonal += 1

  def win(self):
    for _, v in self.nums_letters.items():
      if v == 3:
        return True
    if self.a1c3_diagonal == 3:
      return True
    if self.a3c1_diagonal == 3:
      return True
    return False


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
    if self != move.for_game:
      raise NotAllowedGame()

    is_x = move.player == self.x_player
    is_o = move.player == self.o_player

    if not is_x and not is_o:
      raise NotAllowedPlayer()

    if (self.state == 'XP' and is_o) or (self.state == 'OP' and is_x):
      raise NotYourTurn()

    move_max_order = 0
    for m in self.moves.all():
      if m.code == move.code:
        raise NotAllowedMove()
      if m.order > move_max_order:
        move_max_order = m.order
    move.order = move_max_order + 1

    move.save()
    self.moves.add(move)

    winner = self.check_winner()

    if winner:
      self.state = winner
    else:
      if self.state == 'XP':
        self.state = 'OP'
      elif self.state == 'OP':
        self.state = 'XP'
      else:
        raise GameException('Game logic error.')

    self.save()

  def check_winner(self):
    x_counter = GameCounter()
    o_counter = GameCounter()

    for move in self.moves.all():
      if move.player == self.x_player:
        x_counter.add_code(move.code)
      elif move.player == self.o_player:
        o_counter.add_code(move.code)
      else:
        raise GameException('Game logic error.')

    if x_counter.win():
      return 'XW'
    elif o_counter.win():
      return 'OW'
    else:
      return None


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
  for_game = models.ForeignKey('game.Game')
  order = models.IntegerField()
  code = models.CharField(max_length=2, choices=CODES)


