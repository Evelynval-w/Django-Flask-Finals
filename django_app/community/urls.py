from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('story/<int:story_id>/rate/', views.rate_story, name='rate'),
    path('story/<int:story_id>/comment/', views.add_comment, name='comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('story/<int:story_id>/report/', views.report_story, name='report'),
]
