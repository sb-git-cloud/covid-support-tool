# Generated by Django 3.0.7 on 2020-06-24 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200624_0045'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='givenName',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='account',
            old_name='name',
            new_name='lastname',
        ),
    ]
