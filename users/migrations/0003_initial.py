# Generated by Django 4.1.1 on 2022-09-09 20:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('preference_id', models.AutoField(primary_key=True, serialize=False)),
                ('theme', models.CharField(choices=[('light', 'Light Theme'), ('dark', 'Dark Theme')], max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='preferences',
            constraint=models.UniqueConstraint(fields=('user',), name='One Entry Per User'),
        ),
    ]