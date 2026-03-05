"""
reviews/views.py - Views for product reviews
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from products.models import Product
from orders.models import OrderItem
from .forms import ReviewForm


@login_required
def create_review(request, product_id):
    """Create a product review"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Check if user has purchased this product
    has_purchased = OrderItem.objects.filter(
        order__user=request.user,
        product=product,
        order__status='completed'
    ).exists()
    
    if not has_purchased:
        messages.error(request, 'Bạn chỉ có thể đánh giá sản phẩm đã mua.')
        return redirect('products:detail', slug=product.slug)
    
    # Check if user already reviewed
    if Review.objects.filter(user=request.user, product=product).exists():
        messages.warning(request, 'Bạn đã đánh giá sản phẩm này rồi.')
        return redirect('products:detail', slug=product.slug)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            
            messages.success(request, 'Cảm ơn bạn đã đánh giá!')
            return redirect('products:detail', slug=product.slug)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'product': product,
    }
    
    return render(request, 'reviews/create_review.html', context)


@login_required
def edit_review(request, review_id):
    """Edit user's review"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã cập nhật đánh giá.')
            return redirect('products:detail', slug=review.product.slug)
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'form': form,
        'review': review,
        'product': review.product,
    }
    
    return render(request, 'reviews/edit_review.html', context)


@login_required
def delete_review(request, review_id):
    """Delete user's review"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Đã xóa đánh giá.')
    
    return redirect('products:detail', slug=product_slug)