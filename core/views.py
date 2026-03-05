# core/views.py - Core views (Home, Dashboard, Analytics)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from products.models import Product, Category
"""
core/views.py - Core views (Home, Dashboard, Analytics)
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from products.models import Product, Category
from orders.models import Order, OrderItem  # ✅ ĐÃ SỬA
from accounts.models import User
from reviews.models import Review


def home_view(request):
    """Homepage view"""
    # ... phần còn lại giữ nguyên
from accounts.models import User
from reviews.models import Review


def home_view(request):
    """Homepage view"""
    # Featured products
    featured_products = Product.objects.filter(
        is_featured=True,
        is_active=True
    )[:6]
    
    # New arrivals
    new_products = Product.objects.filter(
        is_active=True
    ).order_by('-created_at')[:8]
    
    # Best sellers
    best_sellers = Product.objects.filter(
        is_active=True
    ).order_by('-sold_count')[:8]
    
    # Active categories
    categories = Category.objects.filter(is_active=True)[:6]
    
    context = {
        'featured_products': featured_products,
        'new_products': new_products,
        'best_sellers': best_sellers,
        'categories': categories,
    }
    
    return render(request, 'core/home.html', context)


@login_required
def admin_dashboard_view(request):
    """Admin dashboard with statistics"""
    if not request.user.is_admin:
        messages.error(request, 'Bạn không có quyền truy cập.')
        return redirect('core:home')
    
    # Date ranges
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)
    last_7_days = today - timedelta(days=7)
    
    # Total statistics
    total_products = Product.objects.filter(is_active=True).count()
    total_users = User.objects.filter(is_active=True, role='user').count()
    total_orders = Order.objects.count()
    
    # Revenue statistics
    total_revenue = Order.objects.filter(
        status='completed'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    revenue_30_days = Order.objects.filter(
        status='completed',
        ordered_at__gte=last_30_days
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    revenue_7_days = Order.objects.filter(
        status='completed',
        ordered_at__gte=last_7_days
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Order statistics by status
    pending_orders = Order.objects.filter(status='pending').count()
    processing_orders = Order.objects.filter(status='processing').count()
    shipping_orders = Order.objects.filter(status='shipping').count()
    
    # Low stock products (< 10)
    low_stock_products = Product.objects.filter(
        is_active=True,
        stock_quantity__lt=10
    ).count()
    
    # Recent orders
    recent_orders = Order.objects.select_related('user').order_by('-ordered_at')[:10]
    
    # Top selling products
    top_products = Product.objects.filter(
        is_active=True
    ).order_by('-sold_count')[:10]
    
    # Revenue by day (last 7 days)
    revenue_by_day = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        revenue = Order.objects.filter(
            status='completed',
            ordered_at__date=date
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        revenue_by_day.append({
            'date': date.strftime('%d/%m'),
            'revenue': float(revenue)
        })
    
    # Orders by status (for chart)
    orders_by_status = []
    for status, label in Order.STATUS_CHOICES:
        count = Order.objects.filter(status=status).count()
        orders_by_status.append({
            'status': label,
            'count': count
        })
    
    context = {
        'total_products': total_products,
        'total_users': total_users,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'revenue_30_days': revenue_30_days,
        'revenue_7_days': revenue_7_days,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'shipping_orders': shipping_orders,
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
        'top_products': top_products,
        'revenue_by_day': revenue_by_day,
        'orders_by_status': orders_by_status,
    }
    
    return render(request, 'core/admin_dashboard.html', context)


@login_required
def analytics_view(request):
    """Detailed analytics page"""
    if not request.user.is_admin:
        messages.error(request, 'Bạn không có quyền truy cập.')
        return redirect('core:home')
    
    # Get date range from request
    days = int(request.GET.get('days', 30))
    start_date = timezone.now().date() - timedelta(days=days)
    
    # Revenue trend
    revenue_trend = []
    for i in range(days - 1, -1, -1):
        date = timezone.now().date() - timedelta(days=i)
        revenue = Order.objects.filter(
            status='completed',
            ordered_at__date=date
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        revenue_trend.append({
            'date': date.strftime('%Y-%m-%d'),
            'revenue': float(revenue)
        })
    
    # Category performance
    category_stats = []
    for category in Category.objects.filter(is_active=True):
        total_sold = Product.objects.filter(
            category=category,
            is_active=True
        ).aggregate(total=Sum('sold_count'))['total'] or 0
        
        revenue = OrderItem.objects.filter(
            product__category=category,
            order__status='completed'
        ).aggregate(total=Sum('subtotal'))['total'] or 0
        
        category_stats.append({
            'name': category.name,
            'sold': total_sold,
            'revenue': float(revenue)
        })
    
    # Top customers
    top_customers = User.objects.filter(
        role='user',
        orders__status='completed'
    ).annotate(
        total_spent=Sum('orders__total_amount'),
        order_count=Count('orders')
    ).order_by('-total_spent')[:10]
    
    context = {
        'days': days,
        'revenue_trend': revenue_trend,
        'category_stats': category_stats,
        'top_customers': top_customers,
    }
    
    return render(request, 'core/analytics.html', context)