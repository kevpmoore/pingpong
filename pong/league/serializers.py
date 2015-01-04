from rest_framework import serializers

from pong.league.models import Game, Player, League, LeaguePlayerMap, Invite


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ('league_name', 'id')


class GameSerializer(serializers.ModelSerializer):
    winner = serializers.SerializerMethodField()
    loser = serializers.SerializerMethodField()

    def get_winner(self, game):
        try:
            league = game.league
            player = PlayerSerializer(game.winner, context={'league': league})
            return player.data
        except Exception, e:
            return None

    def get_loser(self, game):
        try:
            league = game.league
            player = PlayerSerializer(game.loser, context={'league': league})
            return player.data
        except Exception, e:
            return None

    class Meta:
        model = Game
        fields = ('winner', 'loser', 'league', 'points')


class PlayerSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    win_count = serializers.SerializerMethodField()
    lose_count = serializers.SerializerMethodField()
    game_count = serializers.SerializerMethodField()

    def get_win_count(self, player):
        try:
            league = self.context['league']
            league_player_map = LeaguePlayerMap.objects.get(player_fk=player, league_fk=league)
            return league_player_map.win_count
        except Exception, e:
            return None

    def get_lose_count(self, player):
        try:
            league = self.context['league']
            league_player_map = LeaguePlayerMap.objects.get(player_fk=player, league_fk=league)
            return league_player_map.lose_count
        except Exception, e:
            return None

    def get_game_count(self, player):
        try:
            league = self.context['league']
            league_player_map = LeaguePlayerMap.objects.get(player_fk=player, league_fk=league)
            return league_player_map.game_count
        except Exception, e:
            return None

    def get_rating(self, player):
        try:
            league = self.context['league']
            league_player_map = LeaguePlayerMap.objects.get(player_fk=player, league_fk=league)
            return league_player_map.rating
        except Exception, e:
            return None

    class Meta:
        model = Player
        fields = ('username','id', 'rating', 'win_count', 'lose_count', 'game_count',)


class InviteSerializer(serializers.ModelSerializer):

    league_name = serializers.SerializerMethodField('get_league_details')
    # from_player = serializers.SerializerMethodField('get_player_details')
    from_player_username = serializers.SerializerMethodField('get_from_username')

    def get_league_details(self, invite):
        try:
            # league = League.objects.get(invite.league_id)
            league_name = invite.league.league_name
            # serialized = LeagueSerializer(league)
            return league_name
        except Exception, e:
            return  None

    def get_from_username(self, invite):
        try:
            return invite.from_player.username
        except Exception, e:
            return None

    class Meta:
        model = Invite
        fields = ('from_player', 'from_player_username', 'to_player', 'id', 'league_name', 'status')