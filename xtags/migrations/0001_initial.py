# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table('xtags_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('promote', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('xtags', ['Tag'])

        # Adding model 'TaggedItem'
        db.create_table('xtags_taggeditem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['xtags.Tag'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='xtags_taggeditem_tagged_items', to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('xtags', ['TaggedItem'])

        # Adding unique constraint on 'TaggedItem', fields ['tag', 'object_id', 'content_type']
        db.create_unique('xtags_taggeditem', ['tag_id', 'object_id', 'content_type_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'TaggedItem', fields ['tag', 'object_id', 'content_type']
        db.delete_unique('xtags_taggeditem', ['tag_id', 'object_id', 'content_type_id'])

        # Deleting model 'Tag'
        db.delete_table('xtags_tag')

        # Deleting model 'TaggedItem'
        db.delete_table('xtags_taggeditem')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'xtags.tag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'promote': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'xtags.taggeditem': {
            'Meta': {'unique_together': "(('tag', 'object_id', 'content_type'),)", 'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'xtags_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['xtags.Tag']"})
        }
    }

    complete_apps = ['xtags']
