# Generated by Django 3.0.7 on 2020-06-23 21:04

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sim', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sim',
            name='datecreated',
        ),
        migrations.RemoveField(
            model_name='sim',
            name='dateupdated',
        ),
        migrations.RemoveField(
            model_name='sim',
            name='mortrate',
        ),
        migrations.RemoveField(
            model_name='sim',
            name='name',
        ),
        migrations.RemoveField(
            model_name='sim',
            name='narrivals',
        ),
        migrations.RemoveField(
            model_name='sim',
            name='patients',
        ),
        migrations.RemoveField(
            model_name='sim',
            name='resources',
        ),
        migrations.RemoveField(
            model_name='sim',
            name='simtime',
        ),
        migrations.RemoveField(
            model_name='sim',
            name='totalmean',
        ),
        migrations.RemoveField(
            model_name='sim',
            name='ventmean',
        ),
        migrations.AddField(
            model_name='sim',
            name='input',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
