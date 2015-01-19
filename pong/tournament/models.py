from django.db import models
from pong.league.models import League, Player


class Tournament(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    league_fk = models.ForeignKey(League)
    tournament_winner = models.CharField(max_length=255)
    is_finished = models.BooleanField(default=False)
    has_pregame = models.BooleanField(default=False)
    cur_round = models.IntegerField(default=1)


class TournamentGame(models.Model):
    round = models.IntegerField(default=1) # belongs to round
    is_final = models.BooleanField(default=False, null=False, blank=False)

    tournament_fk = models.ForeignKey(Tournament, related_name='game_set')

    home_player = models.ForeignKey(Player, related_name='home_player')
    away_player = models.ForeignKey(Player, related_name='away_player')
    
    winner = models.ForeignKey(Player, related_name='winner_player')


class TournamentPlayerMap(models.Model):
    round = models.IntegerField(default=1) #meta round
    still_in = models.BooleanField(default=True)
    rating = models.IntegerField()

    tournament_fk = models.ForeignKey(Tournament)
    player_fk = models.ForeignKey(Player)

