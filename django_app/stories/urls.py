from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('', views.story_list, name='list'),
    path('story/<int:story_id>/', views.story_detail, name='detail'),
    path('about/', views.about, name='about'),
    path('help/', views.help_page, name='help'),
]
