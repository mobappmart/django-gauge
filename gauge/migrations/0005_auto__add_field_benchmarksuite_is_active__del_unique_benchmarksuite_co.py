# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'BenchmarkSuite', fields ['control', 'benchmark_runs', 'experiment', 'repository']
        db.delete_unique('gauge_benchmarksuite', ['control_id', 'benchmark_runs', 'experiment_id', 'repository_id'])

        # Adding field 'BenchmarkSuite.is_active'
        db.add_column('gauge_benchmarksuite', 'is_active', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding unique constraint on 'BenchmarkSuite', fields ['control', 'benchmark_runs', 'experiment', 'python_version', 'repository']
        db.create_unique('gauge_benchmarksuite', ['control_id', 'benchmark_runs', 'experiment_id', 'python_version_id', 'repository_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'BenchmarkSuite', fields ['control', 'benchmark_runs', 'experiment', 'python_version', 'repository']
        db.delete_unique('gauge_benchmarksuite', ['control_id', 'benchmark_runs', 'experiment_id', 'python_version_id', 'repository_id'])

        # Deleting field 'BenchmarkSuite.is_active'
        db.delete_column('gauge_benchmarksuite', 'is_active')

        # Adding unique constraint on 'BenchmarkSuite', fields ['control', 'benchmark_runs', 'experiment', 'repository']
        db.create_unique('gauge_benchmarksuite', ['control_id', 'benchmark_runs', 'experiment_id', 'repository_id'])


    models = {
        'gauge.benchmark': {
            'Meta': {'ordering': "['name']", 'object_name': 'Benchmark'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'gauge.benchmarkresult': {
            'Meta': {'ordering': "['benchmark__name', 'run_date']", 'object_name': 'BenchmarkResult'},
            'avg_base': ('django.db.models.fields.FloatField', [], {}),
            'avg_changed': ('django.db.models.fields.FloatField', [], {}),
            'benchmark': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gauge.Benchmark']"}),
            'delta_avg': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'delta_min': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'delta_std': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_base': ('django.db.models.fields.FloatField', [], {}),
            'min_changed': ('django.db.models.fields.FloatField', [], {}),
            'raw': ('django.db.models.fields.TextField', [], {}),
            'run_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'significant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'std_base': ('django.db.models.fields.FloatField', [], {}),
            'std_changed': ('django.db.models.fields.FloatField', [], {}),
            'suite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gauge.BenchmarkSuite']"})
        },
        'gauge.benchmarksuite': {
            'Meta': {'unique_together': "(['python_version', 'repository', 'control', 'experiment', 'benchmark_runs'],)", 'object_name': 'BenchmarkSuite'},
            'benchmark_runs': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1000'}),
            'benchmarks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['gauge.Benchmark']", 'through': "orm['gauge.BenchmarkResult']", 'symmetrical': 'False'}),
            'control': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'control_set'", 'to': "orm['gauge.Branch']"}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'experiment_set'", 'to': "orm['gauge.Branch']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'python_version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gauge.PythonVersion']"}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gauge.Repository']"})
        },
        'gauge.branch': {
            'Meta': {'object_name': 'Branch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'gauge.pythonversion': {
            'Meta': {'object_name': 'PythonVersion'},
            'binary': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'gauge.repository': {
            'Meta': {'object_name': 'Repository'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'vcs_type': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['gauge']
