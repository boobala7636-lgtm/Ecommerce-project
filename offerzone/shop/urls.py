from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('register/',views.register, name='register'),
    path('login/',views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('collections-page/', views.collections, name='collections'),
    path('product/<str:name>/', views.productview, name='product'),
    path('product-details/<str:cname>/<str:pname>/',views.product_details, name='product_details'),
    path('add_to_cart/',views.add_to_cart, name='add_to_cart'),
    path('cart-details/', views.cart_display, name='cart_details'),
    path('remove-cart/<str:id>/', views.remove_cart, name='remove_cart'),

]