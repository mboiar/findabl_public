from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

from . import settings
from places.urls import place_patterns
from users.views import toggle_mode_preference
from users.urls import user_patterns, registration_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('toggle_mode_preference/', toggle_mode_preference, name='toggle_mode_preference'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include(place_patterns,namespace='places')),
    path('users/', include(user_patterns,namespace='users')),
    path('', include(registration_patterns, namespace='reg'))
)