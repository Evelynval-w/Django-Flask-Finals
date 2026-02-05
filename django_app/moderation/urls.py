from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('stories/', views.story_list, name='story_list'),
    path('stories/<int:story_id>/suspend/', views.suspend_story, name='suspend_story'),
    path('stories/<int:story_id>/unsuspend/', views.unsuspend_story, name='unsuspend_story'),
]
