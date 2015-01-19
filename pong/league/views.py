from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
import requests, json

from decorators import league_membership_required
from models import League, Player, Game, LeaguePlayerMap, Invite, INV_PENDING, \
    INV_ACCEPTED, INV_DECLINED
from pong.league.serializers import GameSerializer, PlayerSerializer, \
    LeagueSerializer, InviteSerializer

import random


class IndexView(TemplateView):

    template_name = 'base.html'


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.DATA['email']
        username = request.DATA['username']
        password = request.DATA['password']

        pre_existing = Player.objects.filter(Q(username__iexact=username) | Q(email__iexact=email))
        if ' ' in username:
            return Response([{'type': 'danger', 'msg': 'Yeah soo.. no spaces in username please. Gracias Amigo.'}], status=status.HTTP_403_FORBIDDEN)
        if username == '' or email == '' or password == '':
            return Response([{'type': 'danger', 'msg': 'All Fields are required buddy'}], status=status.HTTP_403_FORBIDDEN)
        if len(pre_existing) is not 0:
            return Response([{'type': 'danger', 'msg': 'username/email already exists.'}], status=status.HTTP_403_FORBIDDEN)
        else:
            player = Player()
            player.email = email
            player.username = username
            player.is_active = True
            player.set_password(password)
            player.save()
            authed = authenticate(username=username, password=password)
            login(request, authed)

            serialized = PlayerSerializer(player)

            return Response(serialized.data, status=status.HTTP_201_CREATED)


class PlayerLeagueView(APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        """
        Get all players leagues
        """
        player = Player.objects.get(id=request.user.id)

        try:
            leagues = player.league_set.all()
        except Exception, e:
            return Response([], status=status.HTTP_404_NOT_FOUND)

        serialized = LeagueSerializer(leagues, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new league.
        """
        league_name = request.DATA['league_name']
        league_pass = request.DATA['league_pass']

        if ' ' in league_name:
            return Response([{'type': 'danger', 'msg': 'Sorry boss, im super lazy.. No spaces in league names yet please.'}], status=status.HTTP_403_FORBIDDEN)
        pre_existing = League.objects.filter(league_name__iexact=league_name)

        if len(pre_existing) is not 0 or league_name == '':
            return Response([{'type': 'danger', 'msg': 'Invalid league name'}], status=status.HTTP_403_FORBIDDEN)

        if league_pass is None or league_pass == '':
            return Response([{'type': 'danger', 'msg': 'League passes are useful.. please add one.'}], status=status.HTTP_403_FORBIDDEN)

        player = Player.objects.get(id=request.user.id)
        league = League.objects.create(league_name=league_name, league_pass=league_pass)

        LeaguePlayerMap.objects.create(league_fk=league, player_fk=player)

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request):
        """
        Delete an existing league.
        """
        pass


class PlayerRankingsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, league_name):
        try:
            league = League.objects.get(league_name__iexact=league_name)
            players = league.player_set.all()

            serialized = PlayerSerializer(players, many=True, context={'league': league})
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serialized.data, status=status.HTTP_200_OK)


class LeagueHistoryView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, league_name):
        """
        Get the last 30 games in a league.
        """
        try:
            league = League.objects.get(league_name__iexact=league_name)
            games = Game.objects.filter(league=league).order_by('-created')[:5]
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        #create serializer
        serialized_data = GameSerializer(games, many=True)

        return Response(serialized_data.data, status=status.HTTP_200_OK)


class LeagueGamesView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @league_membership_required
    def post(self, request):
        """
        Add a new game to a league.
        """
        win_msg = (
            'OooOoo, kill \'em',
            'Nice ! Moving up in the world.',
            'If winning isnt everything, why are we keeping score?',
            'BOOOM',
            'They hate us, coz they aint us',
            'Whoever said, \'It\'s not whether you win or lose that counts.\' probably lost.',
            'Champions are made at the Ping Pong Table !',
            'Inviiiiincible',
            'Victory lasts only through the life time, but excellence lasts forever.',
            'Awesome, now get back to work slacker !',
            'Let\'s make a habit of it',
            'You\'re now that little bit extra awesome.'
        )

        league_name = request.DATA['league_name']
        loser = request.DATA['loser']

        if loser == '' or loser is None:
            return Response([{'type': 'warning', 'msg': 'err.. you can\'t play nobody.. they don\'t exist'}], status=status.HTTP_403_FORBIDDEN)
        try:
            player_w = Player.objects.get(id=request.user.id)
            player_l = Player.objects.get(username__iexact=loser)

            if player_l.id is player_w.id:
                return Response([{'type': 'danger', 'msg': 'No. Just No. You cannot play yourself !'}], status=status.HTTP_403_FORBIDDEN)

            league = League.objects.get(league_name__iexact=league_name)

            # ensure both player belong to this league !!
            #increment game counts
            new_game = Game.objects.create(
                winner=player_w,
                loser=player_l,
                league=league
            )
        except Exception, e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        new_game.adjust_meta_data()
        new_game.save()

        r = random.randint(0, len(win_msg)-1)

        return Response([{'type': 'success', 'msg': win_msg[r]}], status=status.HTTP_200_OK)


class LeagueJoinView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        league_name = request.DATA['league_name']
        league_pass = request.DATA['league_pass']
        player = Player.objects.get(id=request.user.id)

        try:
            league = League.objects.get(league_name__iexact=league_name, league_pass=league_pass)
            if league is not None:
                try:
                    LeaguePlayerMap.objects.get(player_fk=player, league_fk=league)
                    return Response([{'type': 'danger', 'msg': 'You\'re already part of this league'}], status=status.HTTP_403_FORBIDDEN)
                except ObjectDoesNotExist:
                    LeaguePlayerMap.objects.create(league_fk=league, player_fk=player)
        except ObjectDoesNotExist:
            return Response([{'type': 'danger', 'msg': 'Sorry boss, wrong league name & pass combo'}], status=status.HTTP_403_FORBIDDEN)

        return Response([{'type': 'success', 'msg': 'You\'re in !'}], status=status.HTTP_202_ACCEPTED)


class CreatePlayerInviteView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @league_membership_required
    def post(self, request):
        """
        Create a new invitation for a user from another user
        """
        from_player = Player.objects.get(id=request.user.id)
        invited_user = request.DATA['invited_user']
        league = League.objects.get(league_name__iexact=request.DATA['league_name'])

        try:
            to_player = Player.objects.get(username__iexact=invited_user)
            belongs_to = to_player.league_set.filter(league_name__iexact=request.DATA['league_name'])

            if len(belongs_to) is not 0:
                return Response([{'type': 'danger', 'msg': 'Looks like they already belong to this league.'}], status=status.HTTP_403_FORBIDDEN)

            inv = Invite.objects.create(
                from_player=from_player,
                to_player=to_player,
                league=league
            )
        except ObjectDoesNotExist:
            return Response([{'type': 'danger', 'msg': 'Yo, I don\'t know who that is. Is the username correct?'}],status=status.HTTP_404_NOT_FOUND)

        return Response([{'type': 'success', 'msg': 'Cool. ' + to_player.username +' is on the list.'}], status=status.HTTP_201_CREATED)


class ActionPlayerInviteView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        action = request.DATA['action']
        league_name = request.DATA['league_name']
        player = Player.objects.get(id=request.user.id)

        try:
            # inv = Invite.objects.get(id=invite_id)
            league = League.objects.get(league_name__iexact=league_name)
            if action == 'accept':
                Invite.objects.filter(league=league, to_player=player).update(status=INV_ACCEPTED)
                LeaguePlayerMap.objects.create(league_fk=league, player_fk=player)
            else:
                Invite.objects.filter(league=league, to_player=player).update(status=INV_DECLINED)

            return Response(status=status.HTTP_200_OK)
        except Exception, e:
            return Response([{'type': 'danger', 'msg': 'Something went wrong. Oopsie'}], status=status.HTTP_200_OK)

    def get(self, request):
        player = Player.objects.get(id=request.user.id)

        try:
            invites = Invite.objects.filter(to_player=player, status=INV_PENDING)
        except Exception, e:
            return Response([], status=status.HTTP_404_NOT_FOUND)

        serialized = InviteSerializer(invites, many=True)
        data = serialized.data
        return Response(data, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        data = {
            'state': request.user.is_authenticated()
        }

        if request.user.is_authenticated:
            player = Player.objects.get(id=request.user.id)
            data['username'] = player.username

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        username = request.DATA['username']
        password = request.DATA['password']

        authed = authenticate(username=username, password=password)

        if authed is not None and authed.is_active:
            login(request, authed)
            try:
                player = Player.objects.get(id=authed.id)
                serialized = PlayerSerializer(player)

                return Response(serialized.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response([{'type': 'danger', 'msg': 'Something went wrong.'}], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response([{'type': 'danger', 'msg': 'Wrong user/pass combo.'}], status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class PlayerView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, league_name, username):
        try:
            player = Player.objects.get(username__iexact=username)
            league = League.objects.get(league_name__iexact=league_name)

            serialized = PlayerSerializer(player, context={'league': league})

            return Response(serialized.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SlackView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        hook = request.DATA['hook']
        msg = request.DATA['msg']

        requests.post(
            hook,
            data=json.dumps({'text': msg}),
            headers={'Content-Type': 'application/json'},
        )

        return Response(status=200)
