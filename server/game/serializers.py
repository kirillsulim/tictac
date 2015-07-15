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


class MoveSerializer(serializers.ModelSerializer):
  class Meta:
    model = Move
    fields = [
      'player',
      'for_game',
      'order',
      'code',
    ]
    
  def create(validated_data):
    return Move(**validated_data)


class GameSerializer(serializers.ModelSerializer):
  moves = MoveSerializer(many=True, read_only=True)

  class Meta:
    model = Game
    fields = [
      'x_player',
      'o_player',
      'state',
      'moves',
      'pk',
    ]





