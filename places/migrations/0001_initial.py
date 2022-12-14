# Generated by Django 4.0.1 on 2022-02-14 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240, verbose_name='Name')),
                ('address', models.CharField(max_length=240, verbose_name='Address')),
                ('url', models.URLField(unique=True, verbose_name='Url on Google Maps')),
                ('score_avg', models.IntegerField(verbose_name='Average Score')),
                ('score_li', models.IntegerField(verbose_name='Light Intensity Score')),
                ('score_so', models.IntegerField(verbose_name='Sound Intensity Score')),
                ('score_sp', models.IntegerField(verbose_name='Spaciousness Score')),
                ('score_sm', models.IntegerField(verbose_name='Smell Intensity Score')),
                ('tag', models.CharField(choices=[('RES', 'Restaurant'), ('BAR', 'Bar'), ('PIZ', 'Pizzeria'), ('CAF', 'Cafe'), ('FAS', 'Fast food')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.place')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
