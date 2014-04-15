# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table(u'ctf_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=255, null=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['ctf.Game'])),
        ))
        db.send_create_signal('ctf', ['Item'])

        # Adding model 'Map'
        db.create_table(u'ctf_map', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=255, null=True)),
            ('radius', self.gf('django.db.models.fields.FloatField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.PortalUser'], null=True)),
        ))
        db.send_create_signal('ctf', ['Map'])

        # Adding model 'Game'
        db.create_table(u'ctf_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('max_players', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('map', self.gf('django.db.models.fields.related.ForeignKey')(related_name='games', to=orm['ctf.Map'])),
            ('visibility_range', self.gf('django.db.models.fields.FloatField')(default=200.0)),
            ('action_range', self.gf('django.db.models.fields.FloatField')(default=5.0)),
        ))
        db.send_create_signal('ctf', ['Game'])

        # Adding M2M table for field players on 'Game'
        m2m_table_name = db.shorten_name(u'ctf_game_players')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('game', models.ForeignKey(orm['ctf.game'], null=False)),
            ('character', models.ForeignKey(orm['core.character'], null=False))
        ))
        db.create_unique(m2m_table_name, ['game_id', 'character_id'])

        # Adding M2M table for field invited_users on 'Game'
        m2m_table_name = db.shorten_name(u'ctf_game_invited_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('game', models.ForeignKey(orm['ctf.game'], null=False)),
            ('portaluser', models.ForeignKey(orm['core.portaluser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['game_id', 'portaluser_id'])


    def backwards(self, orm):
        # Deleting model 'Item'
        db.delete_table(u'ctf_item')

        # Deleting model 'Map'
        db.delete_table(u'ctf_map')

        # Deleting model 'Game'
        db.delete_table(u'ctf_game')

        # Removing M2M table for field players on 'Game'
        db.delete_table(db.shorten_name(u'ctf_game_players'))

        # Removing M2M table for field invited_users on 'Game'
        db.delete_table(db.shorten_name(u'ctf_game_invited_users'))


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.character': {
            'Meta': {'object_name': 'Character'},
            'health': ('django.db.models.fields.DecimalField', [], {'default': '1.0', 'max_digits': '3', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'characters'", 'to': "orm['core.PortalUser']"})
        },
        'core.portaluser': {
            'Meta': {'object_name': 'PortalUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'device_id': ('django.db.models.fields.IntegerField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'device_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'nick': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'ctf.game': {
            'Meta': {'object_name': 'Game'},
            'action_range': ('django.db.models.fields.FloatField', [], {'default': '5.0'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invited_users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pending_games'", 'symmetrical': 'False', 'to': "orm['core.PortalUser']"}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games'", 'to': "orm['ctf.Map']"}),
            'max_players': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'joined_games'", 'symmetrical': 'False', 'to': "orm['core.Character']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'visibility_range': ('django.db.models.fields.FloatField', [], {'default': '200.0'})
        },
        'ctf.item': {
            'Meta': {'object_name': 'Item'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['ctf.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'ctf.map': {
            'Meta': {'object_name': 'Map'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PortalUser']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'radius': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['ctf']