from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product

def product_list(request):
    """Hiển thị tất cả sản phẩm"""
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    
    # Phân trang
    paginator = Paginator(products, 12)  # 12 sản phẩm mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'title': 'Tất cả sản phẩm'
    }
    return render(request, 'products/list.html', context)

def category_view(request, slug):
    """Hiển thị sản phẩm theo danh mục"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True).order_by('-created_at')
    
    # Phân trang
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': page_obj,
        'title': category.name
    }
    return render(request, 'products/category.html', context)

def product_detail(request, slug):
    """Hiển thị chi tiết sản phẩm"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Lấy sản phẩm liên quan (cùng danh mục)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
        'title': product.name
    }
    return render(request, 'products/detail.html', context)