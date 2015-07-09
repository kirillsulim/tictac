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


class MoveSerializer(serializers.Serializer):
  player = serializers.IntegerField()
  for_game = serializers.IntegerField()
  order = serializers.IntegerField()
  code = serializers.CharField(max_length=2)

  def create(validated_data):
    return Move(**validated_data)


