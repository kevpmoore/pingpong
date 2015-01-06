# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'LeaguePlayerMap.win_streak'
        db.add_column(u'league_leagueplayermap', 'win_streak',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'LeaguePlayerMap.lose_streak'
        db.add_column(u'league_leagueplayermap', 'lose_streak',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'LeaguePlayerMap.longest_win_streak'
        db.add_column(u'league_leagueplayermap', 'longest_win_streak',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'LeaguePlayerMap.longest_lose_streak'
        db.add_column(u'league_leagueplayermap', 'longest_lose_streak',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'LeaguePlayerMap.win_streak'
        db.delete_column(u'league_leagueplayermap', 'win_streak')

        # Deleting field 'LeaguePlayerMap.lose_streak'
        db.delete_column(u'league_leagueplayermap', 'lose_streak')

        # Deleting field 'LeaguePlayerMap.longest_win_streak'
        db.delete_column(u'league_leagueplayermap', 'longest_win_streak')

        # Deleting field 'LeaguePlayerMap.longest_lose_streak'
        db.delete_column(u'league_leagueplayermap', 'longest_lose_streak')


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
        u'league.game': {
            'Meta': {'object_name': 'Game'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['league.League']"}),
            'loser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'loser'", 'to': u"orm['league.Player']"}),
            'points': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'winner'", 'to': u"orm['league.Player']"})
        },
        u'league.invite': {
            'Meta': {'object_name': 'Invite'},
            'from_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inviter'", 'to': u"orm['league.Player']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['league.League']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'to_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invited'", 'to': u"orm['league.Player']"})
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
        }
    }

    complete_apps = ['league']