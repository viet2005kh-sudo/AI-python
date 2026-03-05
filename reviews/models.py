"""
Models for product reviews
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """Product review model"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Người dùng'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Sản phẩm'
    )
    
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Đánh giá'
    )
    title = models.CharField(max_length=200, blank=True, verbose_name='Tiêu đề')
    content = models.TextField(verbose_name='Nội dung')
    image = models.ImageField(
        upload_to='reviews/',
        blank=True,
        null=True,
        verbose_name='Hình ảnh'
    )
    
    helpful_count = models.IntegerField(default=0, verbose_name='Hữu ích')
    is_verified_purchase = models.BooleanField(
        default=False,
        verbose_name='Mua hàng đã xác thực'
    )
    is_approved = models.BooleanField(default=True, verbose_name='Đã duyệt')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'reviews'
        verbose_name = 'Đánh giá'
        verbose_name_plural = 'Đánh giá'
        unique_together = ['user', 'product']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', 'is_approved']),
            models.Index(fields=['-rating']),
        ]
    
    def __str__(self):
        return f"{self.user.full_name} - {self.product.name} ({self.rating}★)"
    
    def save(self, *args, **kwargs):
        # Check if user has purchased this product
        if not self.is_verified_purchase:
            from orders.models import OrderItem
            has_purchased = OrderItem.objects.filter(
                order__user=self.user,
                product=self.product,
                order__status='completed'
            ).exists()
            self.is_verified_purchase = has_purchased
        
        super().save(*args, **kwargs)
        
        # Update product rating
        self.product.update_rating()
    
    def delete(self, *args, **kwargs):
        product = self.product
        super().delete(*args, **kwargs)
        # Update product rating after deletion
        product.update_rating()
    
    @property
    def stars_display(self):
        """Return stars as string"""
        return '★' * self.rating + '☆' * (5 - self.rating)