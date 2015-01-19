# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tournament'
        db.create_table(u'tournament_tournament', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('league_fk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['league.League'])),
            ('tournament_winner', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_pregame', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cur_round', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'tournament', ['Tournament'])

        # Adding model 'TournamentGame'
        db.create_table(u'tournament_tournamentgame', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('round', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('is_final', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tournament_fk', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_set', to=orm['tournament.Tournament'])),
            ('home_player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='home_player', to=orm['league.Player'])),
            ('away_player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='away_player', to=orm['league.Player'])),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='winner_player', to=orm['league.Player'])),
        ))
        db.send_create_signal(u'tournament', ['TournamentGame'])

        # Adding model 'TournamentPlayerMap'
        db.create_table(u'tournament_tournamentplayermap', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('round', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('still_in', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('rating', self.gf('django.db.models.fields.IntegerField')()),
            ('tournament_fk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournament.Tournament'])),
            ('player_fk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['league.Player'])),
        ))
        db.send_create_signal(u'tournament', ['TournamentPlayerMap'])


    def backwards(self, orm):
        # Deleting model 'Tournament'
        db.delete_table(u'tournament_tournament')

        # Deleting model 'TournamentGame'
        db.delete_table(u'tournament_tournamentgame')

        # Deleting model 'TournamentPlayerMap'
        db.delete_table(u'tournament_tournamentplayermap')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'league.league': {
            'Meta': {'object_name': 'League'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'league_pass': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'league_set'", 'symmetrical': 'False', 'through': u"orm['league.LeaguePlayerMap']", 'to': u"orm['league.Player']"})
        },
        u'league.leagueplayermap': {
            'Meta': {'object_name': 'LeaguePlayerMap'},
            'game_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['league.League']", 'db_column': "'league_fk'"}),
            'longest_lose_streak': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'longest_win_streak': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lose_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lose_streak': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'player_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['league.Player']", 'db_column': "'player_fk'"}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '1000'}),
            'win_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'win_streak': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'league.player': {
            'Meta': {'object_name': 'Player', '_ormbases': [u'auth.User']},
            'leagues': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'player_set'", 'to': u"orm['league.League']", 'through': u"orm['league.LeaguePlayerMap']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'tournament.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'cur_round': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'has_pregame': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'league_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['league.League']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'tournament_winner': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'tournament.tournamentgame': {
            'Meta': {'object_name': 'TournamentGame'},
            'away_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_player'", 'to': u"orm['league.Player']"}),
            'home_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_player'", 'to': u"orm['league.Player']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_final': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'round': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'tournament_fk': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_set'", 'to': u"orm['tournament.Tournament']"}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'winner_player'", 'to': u"orm['league.Player']"})
        },
        u'tournament.tournamentplayermap': {
            'Meta': {'object_name': 'TournamentPlayerMap'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['league.Player']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'round': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'still_in': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tournament_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournament.Tournament']"})
        }
    }

    complete_apps = ['tournament']