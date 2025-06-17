from django.urls import path
from . import views

app_name = 'cities'

urlpatterns = [
    path('', views.city_list, name='city_list'),
    path('<int:pk>/', views.city_detail, name='city_detail'),
]
