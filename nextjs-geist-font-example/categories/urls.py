from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('city/<int:city_id>/', views.category_list, name='category_list_by_city'),
    path('<slug:slug>/', views.category_detail, name='category_detail'),
]
