# Generated by Django 4.0.1 on 2022-02-16 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0007_review_delete_rating_review_one rating per place'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='location',
            field=models.CharField(choices=[('WBIE', 'Warszawa-Bielany'), ('WCEN', 'Warszawa-Centrum'), ('WOCH', 'Warszawa-Ochota'), ('WTAR', 'Warszawa-Targówek'), ('WMOK', 'Warszawa-Mokotów'), ('WWOL', 'Warszawa-Wola')], default=('OTHER', 'Other'), max_length=4, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='review',
            name='score_li',
            field=models.IntegerField(choices=[(0, 'Do not know'), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], max_length=20, verbose_name='Light intensity score'),
        ),
        migrations.AlterField(
            model_name='review',
            name='score_sm',
            field=models.IntegerField(choices=[(0, 'Do not know'), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='Smell intensity score'),
        ),
        migrations.AlterField(
            model_name='review',
            name='score_so',
            field=models.IntegerField(choices=[(0, 'Do not know'), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], max_length=20, verbose_name='Sound intensity score'),
        ),
        migrations.AlterField(
            model_name='review',
            name='score_sp',
            field=models.IntegerField(choices=[(0, 'Do not know'), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='Spaciousness score'),
        ),
    ]