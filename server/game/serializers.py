from django.forms import widgets
from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = [
      'pk',
      'username',
    ]

class InviteSerializer(serializers.ModelSerializer):
  class Meta:
    model = Invite
    fields = [
      'pk',
      'from_player',
      'to_player',
      'state',
      'game',
    ]

class GameSerializer(serializers.ModelSerializer):
  class Meta:
    model = Game
    fields = [
      'x_player',
      'o_player',
      'state',
    ]


class MoveSerializer(serializers.ModelSerializer):
  class Meta:
    model = Move
    fields = [
      'player',
      'game',
      'order',
      'code',
    ]

