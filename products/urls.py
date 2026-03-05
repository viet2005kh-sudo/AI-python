from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),  # Danh sách tất cả sản phẩm
    path('category/<slug:slug>/', views.category_view, name='category'),  # Sản phẩm theo danh mục
    path('<slug:slug>/', views.product_detail, name='detail'),  # Chi tiết sản phẩm
]