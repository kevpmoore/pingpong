from rest_framework import serializers

from pong.tournament.models import *
from pong.league.serializers import PlayerSerializer, LeagueSerializer


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('name', 'league_fk', 'tournament_winner', 'is_finished', 'has_pregame', 'cur_round')

    league_fk = serializers.SerializerMethodField()

    def get_league_fk(self):
        try:
            return LeagueSerializer(self.league_fk).data
        except Exception, e:
            return None


class TournamentGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentGame
        fields = ('round', 'is_final', 'tournament_fk', 'home_player', 'away_player', 'winner')

    tournament_fk = serializers.SerializerMethodField()
    home_player = serializers.SerializerMethodField()
    away_player = serializers.SerializerMethodField()

    winner = serializers.SerializerMethodField()

    def get_home_player(self):
        try:
            return PlayerSerializer(self.home_player).data
        except Exception, e:
            return None

    def get_away_player(self):
        try:
            return PlayerSerializer(self.away_player).data
        except Exception, e:
            return None

    def get_winner(self):
        try:
            return PlayerSerializer(self.winner).data
        except Exception, e:
            return None

    def get_tournament_fk(self):
        try:
            return TournamentSerializer(self.tournament_fk).data
        except Exception, e:
            return None