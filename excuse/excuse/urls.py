from django.urls import path

from . import views

app_name = 'excuse'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('board/create/<int:question_id>/', views.board_create, name='board_create'),
    path('excuse/create/', views.excuse_create, name='excuse_create'),
    path('excuse/modify/<int:question_id>/', views.excuse_modify, name='excuse_modify'),
    path('excuse/delete/<int:question_id>/', views.excuse_delete, name='excuse_delete'),
    path('board/modify/<int:answer_id>/', views.board_modify, name='board_modify'),
    path('board/delete/<int:answer_id>/', views.board_delete, name='board_delete'),
]