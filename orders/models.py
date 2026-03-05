"""
Models for orders and shopping cart
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
import uuid


class Cart(models.Model):
    """Shopping cart model"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Người dùng'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        verbose_name='Sản phẩm'
    )
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Số lượng'
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày thêm')
    
    class Meta:
        db_table = 'cart_items'
        verbose_name = 'Giỏ hàng'
        verbose_name_plural = 'Giỏ hàng'
        unique_together = ['user', 'product']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.product.name}"
    
    @property
    def subtotal(self):
        """Calculate subtotal for this cart item"""
        return self.product.get_price * self.quantity
    
    def is_stock_available(self):
        """Check if requested quantity is available"""
        return self.quantity <= self.product.stock_quantity


class Order(models.Model):
    """Order model"""
    
    STATUS_CHOICES = (
        ('pending', 'Chờ xác nhận'),
        ('processing', 'Đang xử lý'),
        ('shipping', 'Đang giao hàng'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
        ('returned', 'Hoàn trả'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('cod', 'Thanh toán khi nhận hàng'),
        ('bank_transfer', 'Chuyển khoản ngân hàng'),
        ('momo', 'Ví MoMo'),
        ('vnpay', 'VNPay'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('unpaid', 'Chưa thanh toán'),
        ('paid', 'Đã thanh toán'),
        ('refunded', 'Đã hoàn tiền'),
    )
    
    # User & Order Info
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Người dùng'
    )
    order_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        verbose_name='Mã đơn hàng'
    )
    
    # Customer Info
    customer_name = models.CharField(max_length=100, verbose_name='Tên khách hàng')
    customer_phone = models.CharField(max_length=20, verbose_name='Số điện thoại')
    customer_email = models.EmailField(blank=True, verbose_name='Email')
    shipping_address = models.TextField(verbose_name='Địa chỉ giao hàng')
    note = models.TextField(blank=True, verbose_name='Ghi chú')
    
    # Financial Info
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name='Tạm tính'
    )
    shipping_fee = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=15000,
        verbose_name='Phí vận chuyển'
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name='Giảm giá'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name='Tổng tiền'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Trạng thái'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cod',
        verbose_name='Phương thức thanh toán'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='unpaid',
        verbose_name='Trạng thái thanh toán'
    )
    
    # Timestamps
    ordered_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày đặt')
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name='Ngày xác nhận')
    shipped_at = models.DateTimeField(null=True, blank=True, verbose_name='Ngày giao')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Ngày hoàn thành')
    cancelled_at = models.DateTimeField(null=True, blank=True, verbose_name='Ngày hủy')
    cancel_reason = models.TextField(blank=True, verbose_name='Lý do hủy')
    
    class Meta:
        db_table = 'orders'
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Đơn hàng'
        ordering = ['-ordered_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['order_number']),
        ]
    
    def __str__(self):
        return self.order_number
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number: ORD-YYYYMMDD-XXXX
            date_str = timezone.now().strftime('%Y%m%d')
            random_str = str(uuid.uuid4().hex[:4]).upper()
            self.order_number = f'ORD-{date_str}-{random_str}'
        
        # Calculate total if not set
        if not self.total_amount or self.total_amount == 0:
            self.calculate_total()
        
        super().save(*args, **kwargs)
    
    def calculate_total(self):
        """Calculate order total"""
        self.total_amount = self.subtotal + self.shipping_fee - self.discount
        
        # Free shipping if subtotal > 200,000
        if self.subtotal >= 200000:
            self.shipping_fee = 0
            self.total_amount = self.subtotal - self.discount
    
    def can_cancel(self):
        """Check if order can be cancelled"""
        return self.status == 'pending'
    
    def can_review(self):
        """Check if order can be reviewed"""
        return self.status == 'completed'
    
    def get_items_count(self):
        """Get total items in order"""
        return self.items.count()
    
    def update_status(self, new_status):
        """Update order status with timestamp"""
        self.status = new_status
        
        if new_status == 'processing':
            self.confirmed_at = timezone.now()
        elif new_status == 'shipping':
            self.shipped_at = timezone.now()
        elif new_status == 'completed':
            self.completed_at = timezone.now()
            self.payment_status = 'paid'
        elif new_status == 'cancelled':
            self.cancelled_at = timezone.now()
        
        self.save()


class OrderItem(models.Model):
    """Order item model - stores product snapshot at purchase time"""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Đơn hàng'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.RESTRICT,
        verbose_name='Sản phẩm'
    )
    
    # Snapshot data
    product_name = models.CharField(max_length=200, verbose_name='Tên sản phẩm')
    product_image = models.CharField(max_length=255, blank=True, verbose_name='Hình ảnh')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Đơn giá')
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Số lượng'
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Thành tiền')
    
    class Meta:
        db_table = 'order_items'
        verbose_name = 'Chi tiết đơn hàng'
        verbose_name_plural = 'Chi tiết đơn hàng'
    
    def __str__(self):
        return f"{self.order.order_number} - {self.product_name}"
    
    def save(self, *args, **kwargs):
        # Save product snapshot
        if not self.product_name:
            self.product_name = self.product.name
        if not self.product_image:
            self.product_image = self.product.get_primary_image() or ''
        if not self.price:
            self.price = self.product.get_price
        
        # Calculate subtotal
        self.subtotal = self.price * self.quantity
        
        super().save(*args, **kwargs)