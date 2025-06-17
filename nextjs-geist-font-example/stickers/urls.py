from django.urls import path
from . import views

app_name = 'stickers'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_sticker, name='create_sticker'),
    path('<int:pk>/', views.sticker_detail, name='sticker_detail'),
    path('<int:pk>/edit/', views.edit_sticker, name='edit_sticker'),
    path('<int:pk>/delete/', views.delete_sticker, name='delete_sticker'),
]
