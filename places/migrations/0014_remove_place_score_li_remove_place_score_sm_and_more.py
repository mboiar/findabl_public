# Generated by Django 4.1.1 on 2022-09-24 19:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0013_remove_place_score_avg_remove_review_score_avg_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='score_li',
        ),
        migrations.RemoveField(
            model_name='place',
            name='score_sm',
        ),
        migrations.RemoveField(
            model_name='place',
            name='score_so',
        ),
        migrations.RemoveField(
            model_name='place',
            name='score_sp',
        ),
        migrations.RemoveField(
            model_name='place',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='review',
            name='score_li',
        ),
        migrations.RemoveField(
            model_name='review',
            name='score_sm',
        ),
        migrations.RemoveField(
            model_name='review',
            name='score_so',
        ),
        migrations.RemoveField(
            model_name='review',
            name='score_sp',
        ),
        migrations.AddField(
            model_name='place',
            name='type',
            field=models.CharField(choices=[('ETH', 'Ethnic'), ('BAR', 'Bar'), ('PIZ', 'Pizzeria'), ('CAF', 'Café'), ('FAS', 'Fast food'), ('RES', 'Restaurant'), ('FAM', 'Family-friendly'), ('OTH', 'Other')], default=('OTH', 'Other'), max_length=30, verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='review',
            name='lsi',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Low-sight friendly'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='noi',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Noise'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='sin',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Sensory intensity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='wac',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Wheelchair accessibility'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='place',
            name='location',
            field=models.CharField(choices=[('MOK', 'MOKOTÓW'), ('PRE', 'PRAGA-POŁUDNIE'), ('URW', 'URSYNÓW'), ('WOL', 'WOLA'), ('BIE', 'BIELANY'), ('TAR', 'TARGÓWEK'), ('SRO', 'ŚRÓDMIEŚCIE'), ('BEM', 'BEMOWO'), ('BIA', 'BIAŁOŁĘKA'), ('OCH', 'OCHOTA'), ('WAW', 'WAWER'), ('PPC', 'PRAGA-PÓŁNOC'), ('URS', 'URSYNÓW'), ('ZOL', 'ŻOLIBORZ'), ('WLO', 'WŁOCHY'), ('WIL', 'WILANÓW'), ('REM', 'REMBERTÓW'), ('WES', 'WESOŁA')], max_length=4, verbose_name='Location'),
        ),
    ]
