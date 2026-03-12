from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.support_chat_view, name='support_chat'),
    path('videos/', views.VideoListView.as_view(), name='video_list'),
    path('calculator/', views.CalculationCreateListView.as_view(), name='calculator'),
]