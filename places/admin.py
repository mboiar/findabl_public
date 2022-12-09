from django.contrib import admin

from .models import Review, Place

admin.site.register([Review, Place])