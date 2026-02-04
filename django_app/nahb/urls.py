from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stories.urls')),
    path('accounts/', include('accounts.urls')),
    path('author/', include('author.urls')),
    path('gameplay/', include('gameplay.urls')),
    path('community/', include('community.urls')),
    path('moderation/', include('moderation.urls')),
]
