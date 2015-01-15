from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models import F, Q, Count

#TODO adjust kfact for ratings level
kFACTOR_HIGH = 35
kFACTOR_AVG = 50
kFACTOR_LOW = 60

INV_PENDING = 0
INV_ACCEPTED = 1
INV_DECLINED = 2


class League(models.Model):
    league_name = models.CharField(max_length=64, unique=True, null=False, blank=False)
    league_pass = models.CharField(max_length=64) # on another day i might encrypt this field

    players = models.ManyToManyField('Player', through='LeaguePlayerMap', related_name='league_set')


class Player(User):
    objects = UserManager()

    leagues = models.ManyToManyField('League', through='LeaguePlayerMap', related_name='player_set', blank=True, null=True)


class Game(models.Model):
    winner = models.ForeignKey(Player, related_name='winner')
    loser = models.ForeignKey(Player, related_name='loser')
    league = models.ForeignKey(League)
    points = models.FloatField(default=0)

    created = models.DateTimeField(auto_now=True)

    def adjust_meta_data(self):
        self.adjust_ratings()
        self.adjust_game_counts()
        self.adjust_streaks()

    def adjust_ratings(self):
        assert(self.winner != self.loser)

        winner_meta = LeaguePlayerMap.objects.get(league_fk=self.league, player_fk=self.winner)
        loser_meta = LeaguePlayerMap.objects.get(league_fk=self.league, player_fk=self.loser)

        expected_winner = 1.0/float(1 + 10**((loser_meta.rating - winner_meta.rating)/400))

        expected_loser = 1.0/float(1 + 10**((winner_meta.rating - loser_meta.rating)/400))

        winner_kfactor = self.get_kfactor(winner_meta.rating)
        loser_kfactor = self.get_kfactor(loser_meta.rating)

        new_winner_rating = winner_meta.rating + (winner_kfactor * (1 - expected_winner))
        new_loser_rating = loser_meta.rating + (loser_kfactor * (0 - expected_loser))

        self.points = new_winner_rating - winner_meta.rating

        winner_meta.rating = new_winner_rating
        loser_meta.rating = new_loser_rating
        winner_meta.save()
        loser_meta.save()

        self.save()

    def adjust_game_counts(self):
        #filter or get ?
        LeaguePlayerMap.objects.filter(league_fk=self.league, player_fk=self.winner).update(
            win_count=F('win_count')+1,
            game_count=F('game_count')+1
        )
        LeaguePlayerMap.objects.filter(league_fk=self.league, player_fk=self.loser).update(
            lose_count=F('lose_count')+1,
            game_count=F('game_count')+1
        )

    def adjust_streaks(self):
        #first adjust the winner
        winner_meta = LeaguePlayerMap.objects.get(league_fk=self.league, player_fk=self.winner)
        winner_meta.win_streak += 1
        winner_meta.lose_streak = 0

        if winner_meta.win_streak > winner_meta.longest_win_streak:
            winner_meta.longest_win_streak = winner_meta.win_streak

        winner_meta.save()

        #then do the same for the loser
        loser_meta = LeaguePlayerMap.objects.get(league_fk=self.league, player_fk=self.loser)
        loser_meta.win_streak = 0
        loser_meta.lose_streak += 1

        if loser_meta.lose_streak > loser_meta.longest_lose_streak:
            loser_meta.longest_lose_streak = loser_meta.lose_streak

        loser_meta.save()

    def get_kfactor(self, player_rating):
        if player_rating < 900:
            return kFACTOR_LOW
        elif player_rating > 1250:
            return kFACTOR_HIGH
        else:
            return kFACTOR_AVG


class LeaguePlayerMap(models.Model):
    rating = models.FloatField(default=1000)
    lose_count = models.IntegerField(default=0)
    game_count = models.IntegerField(default=0)
    win_count = models.IntegerField(default=0)

    #stats
    win_streak = models.IntegerField(default=0)
    lose_streak = models.IntegerField(default=0)
    longest_win_streak = models.IntegerField(default=0)
    longest_lose_streak = models.IntegerField(default=0)
    # easy_pickings = models.CharField(max_length=128)
    # easy_picking_games = None

    # rival = models.ForeignKey(Player, related_name='rival')
    # most_feared = models.ForeignKey(Player, related_name='feared')

    player_fk = models.ForeignKey(Player, db_column='player_fk')
    league_fk = models.ForeignKey(League, db_column='league_fk')

    # @property
    # def easy_pickings(self):
    #     try:
    #         ret = Game.objects.filter(winner=self.player_fk).annotate(c=Count('loser')).order_by('-c')[0]
    #         return ret.loser.username
    #     except Exception, e:
    #         return None
    #
    # @property
    # def should_fear(self):
    #     try:
    #         ret = Game.objects.filter(loser=self.player_fk).annotate(c=Count('winner')).order_by('-c')[0]
    #         return ret.winner.username
    #     except Exception, e:
    #         return None

    # @property
    # def rival(self):
    #     try:
    #         games = Game.objects.filter(Q(winner=self) | Q(loser=self)).or
    #     except Exception, e:
    #         return None


class Invite(models.Model):
    league = models.ForeignKey(League)
    from_player = models.ForeignKey(Player, related_name='inviter')
    to_player = models.ForeignKey(Player, related_name='invited')
    status = models.IntegerField(default=INV_PENDING)