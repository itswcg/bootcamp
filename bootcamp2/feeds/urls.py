from django.urls import path
from . import views

urlpatterns = [
    path('', views.feeds, name='feeds'),
    path('like/', views.like, name='like'),
    path('post/', views.post, name='posts'),
    path('load/', views.load, name='load'),
    path('check/', views.check, name='check'),
    path('update/', views.update, name='update'),
    path('comment/', views.comment, name='comment'),
    path('remove/', views.remove, name='remove_feed'),
    path('load_new/', views.load_new, name='load_new'),
    path('track_comments/', views.track_comments, name='track_comments'),
    path('<int:pk>', views.feed, name='feed'),
]
