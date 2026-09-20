from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('collections-page/', views.collections, name='collections'),
    path('product/<str:name>/', views.productview, name='product'),
    path('product-details/<str:cname>/<str:pname>/',views.product_details, name='product_details'),


]