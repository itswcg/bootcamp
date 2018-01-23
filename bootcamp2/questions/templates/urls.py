from django.urls import path

from . import views

urlpatterns = [
    path('', views.questions, name='questions'),
    path('<int:pk>/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('all/', views.all_question, name='all'),
    path('answered/', views.answered, name='answered'),
    path('unanswered/', views.unanswered, name='unanswered'),
    path('answer/', views.answer, name='answer'),

]
