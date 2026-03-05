from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/<str:order_number>/', views.order_success_view, name='order_success'),
    path('order/<str:order_number>/', views.order_detail_view, name='order_detail'),
    path('order/<str:order_number>/cancel/', views.cancel_order_view, name='cancel_order'),
    path('admin/orders/', views.admin_order_list_view, name='admin_order_list'),
]
