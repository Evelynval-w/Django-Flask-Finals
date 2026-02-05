from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stories.urls')),
    path('accounts/', include('accounts.urls')),
    path('author/', include('author.urls')),
    path('play/', include('gameplay.urls')),  # Changed from 'gameplay/' to 'play/'
    path('gameplay/', include('gameplay.urls')),  # Keep this too for backwards compatibility
    path('community/', include('community.urls')),
    path('moderation/', include('moderation.urls')),
]