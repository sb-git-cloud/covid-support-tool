# Generated by Django 3.0.7 on 2020-06-25 20:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sim', '0005_auto_20200625_0233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sim',
            name='input',
        ),
        migrations.AddField(
            model_name='sim',
            name='er_nct',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='er_nmri',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='er_nxray',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='highRiskIcuLos',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='highRiskLos',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='highRiskVentLos',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='icu_nct',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='icu_nmri',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='icu_nxray',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='lowRiskIcuLos',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='lowRiskLos',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='lowRiskVentLos',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='medRiskIcuLos',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='medRiskLos',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='medRiskVentLos',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='mortrate_erhr',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='mortrate_erlr',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='mortrate_ermr',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='mortrate_icuhr',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='mortrate_iculr',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='mortrate_icumr',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='mortrate_wardhr',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='mortrate_wardlr',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='mortrate_wardmr',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='narrivalsHR',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='narrivalsLR',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='narrivalsMR',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='tend',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='ward_nct',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='ward_nmri',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sim',
            name='ward_nxray',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50)]),
            preserve_default=False,
        ),
    ]
