from django.urls import path

from . import views

urlpatterns = [
    path('', views.articles, name='articles'),
    path('write/', views.write, name='write'),
    path('preview/', views.preview, name='preview'),
    path('drafts/', views.drafts, name='drafts'),
    path('comment/', views.comment, name='comment'),
    path('tag/<tag_name>/', views.tag, name='tag'),
    path('edit/<article_id>/', views.edit, name='edit_article'),
    path('<slug>/', views.article, name='article'),
]
