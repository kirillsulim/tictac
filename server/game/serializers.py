from django.forms import widgets
from rest_framework import serializers

from .models import *


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

