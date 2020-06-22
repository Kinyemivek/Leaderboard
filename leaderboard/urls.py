from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page_view, name='home_page'),
    path('board/upload/', views.board_page_upload, name='board_edit'),
    path('board/<str:board_id>/', views.board_page_view, name='board_view'),
    path('board/<str:board_id>/edit/', views.board_page_edit_view, name='board_edit'),
]
