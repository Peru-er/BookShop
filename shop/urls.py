
from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
]
