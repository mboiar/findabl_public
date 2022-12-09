# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
# Create your models here.
# class User(AbstractUser):
# 	pass

class Preferences(models.Model):
    
    themes = (
        ('light', 'Light Theme'),
        ('dark', 'Dark Theme'),
    )
    
    preference_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    theme = models.CharField(max_length=255, choices=themes)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)