from django.urls import path
from . import views

app_name = 'author'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_story, name='create_story'),
    path('story/<int:story_id>/', views.edit_story, name='edit_story'),
    path('story/<int:story_id>/delete/', views.delete_story, name='delete_story'),
    path('story/<int:story_id>/publish/', views.publish_story, name='publish_story'),
    path('story/<int:story_id>/preview/', views.preview_story, name='preview_story'),
    path('story/<int:story_id>/page/add/', views.add_page, name='add_page'),
    path('story/<int:story_id>/page/<int:page_id>/', views.edit_page, name='edit_page'),
    path('story/<int:story_id>/page/<int:page_id>/delete/', views.delete_page, name='delete_page'),
    path('story/<int:story_id>/page/<int:page_id>/set-start/', views.set_start_page, name='set_start_page'),
    path('story/<int:story_id>/page/<int:page_id>/choice/add/', views.add_choice, name='add_choice'),
    path('story/<int:story_id>/page/<int:page_id>/choice/<int:choice_id>/delete/', views.delete_choice, name='delete_choice'),
]
