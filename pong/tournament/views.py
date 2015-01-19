from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from models import Tournament, TournamentGame, TournamentPlayerMap
from serializers import *
from pong.league.models import League, LeaguePlayerMap, Player


class TournamentGamesView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, tournament_name):
        """
        Get all the tournaments games
        """
        try:
            tournament = Tournament.objects.get(tournament_name=tournament_name)

            games = TournamentGame.objects.filter(tournament_fk=tournament)

            serialized = TournamentGame(games, many=True)

            return Response(serialized.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response()

    def patch(self, request):
        """
        Complete a game
        """
        try:
            tournament_name = request.DATA['tournament_name']
            winner_name = request.DATA['winner_name']
            loser_name = request.DATA['loser_name']

            winner = Player.objects.get(username=winner_name)
            loser = Player.objects.get(username=loser_name)
            tournament = Tournament.objects.get(tournament_name=tournament_name)

            game = TournamentGame.objects.get(
                Q(home_player=winner, away_player=loser) | Q(home_player=loser, away_player=winner),
                tournament_fk=tournament,
            )

            game.winner = winner
            game.save()

            winner_meta = TournamentPlayerMap.objects.get(tournament_fk=tournament, player_fk=winner)
            winner_meta.round = tournament.cur_round + 1
            winner_meta.save()

            #after update, if all games played and is not final create next round
            remaining_games = TournamentGame.objects.filter(
                tournament_fk=tournament,
                round=tournament.cur_round,
                winner__isnull=True).count()

            if remaining_games == 0 and not game.is_final:
                create_next_round(tournament, tournament.cur_round + 1)
            elif game.is_final:
                tournament.is_finished = True
                tournament.tournament_winner = winner.username
                tournament.save()
            #if is final update tournament - mark as completed

            return Response(status=status.HTTP_200_OK)
        except Exception, e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TournamentFeature(APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self):
        return Response(True, status=status.HTTP_200_OK)


class TournamentView(APIView):
    
    permission_classes = (permissions.AllowAny,)

    def get(self, request, league_name):
        """
        Get all the tournaments for this league
        """
        league = League.objects.get(league_name=league_name)
        tournaments = Tournament.objects.filter(league_fk=league)

        serialized = TournamentSerializer(tournaments, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates a new tournament based on player numbers and standings
        """
        league_name = request.DATA['league_name']
        tournament_name = request.DATA['tournament_name']

        if tournament_name == '' or tournament_name is None:
            return Response({'msg': 'Invalid or existing tournament name', 'type': 'danger'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            league = League.objects.get(league_name=league_name)

            tournament = Tournament.objects.create(name=tournament_name, league_fk=league)

            league_player_metas = LeaguePlayerMap.objects.filter(league_fk=league)

            for player_meta in league_player_metas:
                TournamentPlayerMap.objects.create(
                    tournament_fk=tournament,
                    player_fk=player_meta.player_fk,
                    round=1,
                    rating=player_meta.rating
                )

            #create the first round
            length = len(tournament)
            if length % 2 is not 0:
                tournament_metas = TournamentPlayerMap.objects.filter(tournament_fk=tournament).order_by('-rating')
                tournament.has_pregame = True
                tournament.cur_round = 0
                tournament.save()

                #create pregame
                tournament_metas[length-1].round = 0
                tournament_metas[length-2].round = 0
                game = TournamentGame.objects.create(
                    round=0,
                    tournament_fk=tournament,
                    home_player=tournament_metas[length-1].player_fk,
                    away_player=tournament_metas[length-2].player_fk
                )
            else:
                create_next_round(tournament, 1)

            return Response(status=status.HTTP_201_CREATED)
        except Exception, e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def create_next_round(tournament, t_round):
    tournament_metas = TournamentPlayerMap.objects.filter(tournament_fk=tournament, round=t_round).order_by('-rating')

    length = len(tournament_metas)
    if length == 6:
        TournamentPlayerMap.objects\
            .filter(player_fk=tournament_metas[0].player_fk)\
            .update(round=t_round+1)

    for n in xrange(length/2):
        game = TournamentGame.objects.create(
            round=t_round,
            tournament_fk=tournament,
            home_player=tournament_metas[n].player_fk,
            away_player=tournament_metas[length - n - 1].player_fk
        )

        if length/2 == 1:
            game.is_final = True
            game.save()