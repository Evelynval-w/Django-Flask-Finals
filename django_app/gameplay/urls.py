from django.urls import path
from . import views

app_name = 'gameplay'

urlpatterns = [
    path('<int:story_id>/', views.play_story, name='play'),
    path('<int:story_id>/choice/', views.make_choice, name='make_choice'),
    path('<int:story_id>/state/', views.game_state, name='game_state'),
    path('<int:story_id>/restart/', views.restart_game, name='restart'),
    path('<int:story_id>/tree/', views.story_tree_data, name='tree_data'),
]
