from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import *
from .serializers import *


class PlayerList(APIView):
  permission_classes = (IsAuthenticated, )

  def get(self, request):
    players = User.objects.exclude(pk=request.user.pk)
    return Response(data=UserSerializer(players, many=True).data)


class InviteList(APIView):
  permission_classes = (IsAuthenticated, )

  def get(self, request):
    invites = Invite.objects.filter(to_player=request.user, state='I')
    return Response(data=InviteSerializer(invites, many=True).data)

  def post(self, request):
    sz = InviteSerializer(data=request.data)
    if sz.is_valid():
      sz.save()
      return Response(data=sz.data, status=status.HTTP_201_CREATED)
    else:
      return Response(data=sz.errors, status=status.HTTP_400_BAD_REQUEST)



class InviteDetailsPermission(permissions.BasePermission):
  """ Allow change invite for inviter and invited only
  """
  def has_object_permission(self, request, view, obj):
    return obj.from_player == request.user or obj.to_player == request.user


class InviteDetails(APIView):
  permission_classes = (InviteDetailsPermission, )

  def get(self, request, pk):
    invite = get_object_or_404(Invite, pk=pk)
    return Response(data=InviteSerializer(invite).data)

  def put(self, request, pk):
    invite = get_object_or_404(Invite, pk=pk)
    if invite.state != 'I':
      return Response(status=status.HTTP_409_CONFLICT)
    sz = InviteSerializer(invite, data=request.data, partial=True)
    if sz.is_valid():
      invite = sz.save()
      if invite.state == 'A':
        invite.game = Game.objects.create(x_player=invite.to_player, o_player=invite.from_player)
        invite.save()
        return Response(data=InviteSerializer(invite).data, status=status.HTTP_202_ACCEPTED)
      else:
        return Response(data=sz.data, status=status.HTTP_202_ACCEPTED)
    else:
      return Response(data=sz.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    invite = get_object_or_404(Invite, pk=pk)
    invite.state = 'D'
    invite.save()
    return Response(status=status.HTTP_200_OK)


class GameList(APIView):
  permission_classes = (IsAuthenticated, )

  def get(self, request):
    games = Game.objects.filter(Q(x_player=request.user) | Q(o_player=request.user))
    sz = GameSerializer(games, many=True)
    return Response(data=sz.data)


class GameDetailsPermission(permissions.BasePermission):
  """ Allow read game info for players
  """

  def has_object_permission(self, request, view, obj):
    return obj.x_player == request.user or obj.o_player == request.user

class GameDetails(APIView):
  permission_classes = (GameDetailsPermission, )

  def get(self, request, pk):
    game = get_object_or_404(Game, pk=pk)
    sz = GameSerializer(game)
    return Response(sz.data)


def make_exception_json(exception):
  res = {
    'error': exception.__class__.__name__,
  }
  return res


class MakeMove(APIView):
  permission_classes = []

  def post(self, request):
    data = JSONParser().parse(request)
    sz = MoveSerializer(data=data, partial=True)
    if sz.is_valid():
      game_pk = sz.validated_data['for_game'].pk
      game = get_object_or_404(Game, pk=game_pk)

      sz.validated_data['for_game'] = game
      move = MoveSerializer.create(sz.validated_data)
      move.player = request.user

      try:
        game.make_move(move)
      except GameException as e:
        return Response(data=make_exception_json(e), status=status.HTTP_406_NOT_ACCEPTABLE)

      sz = GameSerializer(game)
      return Response(sz.data, status=status.HTTP_202_ACCEPTED)
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)









