from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, Order, OrderItem
from products.models import Product


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    subtotal = sum(item.subtotal for item in cart_items)
    shipping_fee = 15000 if subtotal < 200000 else 0
    total = subtotal + shipping_fee
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_fee': shipping_fee,
        'total': total,
    }
    return render(request, 'orders/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    if not product.is_in_stock:
        messages.error(request, 'Sản phẩm đã hết hàng.')
        return redirect('products:detail', slug=product.slug)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > product.stock_quantity:
        messages.error(request, f'Chỉ còn {product.stock_quantity} sản phẩm trong kho.')
        return redirect('products:detail', slug=product.slug)
    
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock_quantity:
            messages.error(request, f'Chỉ còn {product.stock_quantity} sản phẩm trong kho.')
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, f'Đã thêm {product.name} vào giỏ hàng!')
    else:
        messages.success(request, f'Đã thêm {product.name} vào giỏ hàng!')
    
    return redirect('orders:cart')


@login_required
def update_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    action = request.POST.get('action')
    
    if action == 'remove':
        cart_item.delete()
        messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng.')
    
    return redirect('orders:cart')


@login_required
def checkout_view(request):
    return render(request, 'orders/checkout.html')


@login_required
def order_success_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_detail_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def cancel_order_view(request, order_number):
    return redirect('accounts:order_history')


@login_required
def admin_order_list_view(request):
    if not request.user.is_admin:
        messages.error(request, 'Bạn không có quyền truy cập.')
        return redirect('core:home')
    orders = Order.objects.all()
    return render(request, 'orders/admin/order_list.html', {'orders': orders})


@login_required
def admin_order_detail_view(request, order_number):
    return redirect('accounts:order_history')


@login_required
def admin_update_order_status(request, order_number):
    return redirect('accounts:order_history')
