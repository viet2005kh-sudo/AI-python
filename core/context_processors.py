"""
core/context_processors.py - Global context variables
"""

from products.models import Category
from orders.models import Cart


def categories_processor(request):
    """Add categories to all templates"""
    categories = Category.objects.filter(is_active=True).order_by('display_order')
    return {
        'global_categories': categories
    }


def cart_processor(request):
    """Add cart count to all templates"""
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
    
    return {
        'cart_count': cart_count
    }