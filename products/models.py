

"""
Models for products and categories
"""

from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Tên danh mục')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Mô tả')
    icon = models.CharField(max_length=50, blank=True, verbose_name='Icon')
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Kích hoạt')
    display_order = models.IntegerField(default=0, verbose_name='Thứ tự hiển thị')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('products:category', kwargs={'slug': self.slug})
    
    def get_products_count(self):
        return self.products.filter(is_active=True).count()


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='products', verbose_name='Danh mục')
    name = models.CharField(max_length=200, unique=True, verbose_name='Tên sản phẩm')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug')
    description = models.TextField(verbose_name='Mô tả')
    price = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(0)], verbose_name='Giá')
    discount_price = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(0)], null=True, blank=True, verbose_name='Giá khuyến mãi')
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='Số lượng tồn kho')
    unit = models.CharField(max_length=20, default='gói', verbose_name='Đơn vị')
    weight_grams = models.IntegerField(null=True, blank=True, verbose_name='Khối lượng (g)')
    sold_count = models.IntegerField(default=0, verbose_name='Đã bán')
    view_count = models.IntegerField(default=0, verbose_name='Lượt xem')
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='Đánh giá trung bình')
    review_count = models.IntegerField(default=0, verbose_name='Số đánh giá')
    is_featured = models.BooleanField(default=False, verbose_name='Nổi bật')
    is_active = models.BooleanField(default=True, verbose_name='Kích hoạt')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'products'
        verbose_name = 'Sản phẩm'
        verbose_name_plural = 'Sản phẩm'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0
    
    @property
    def is_on_sale(self):
        return self.discount_price and self.discount_price < self.price
    
    @property
    def get_price(self):
        if self.is_on_sale:
            return self.discount_price
        return self.price
    
    @property
    def discount_percent(self):
        if self.is_on_sale:
            return int((1 - float(self.discount_price) / float(self.price)) * 100)
        return 0
    
    def get_primary_image(self):
        image = self.images.filter(is_primary=True).first()
        if not image:
            image = self.images.first()
        return image.image.url if image else None
    
    def update_rating(self):
        from django.db.models import Avg, Count
        stats = self.reviews.filter(is_approved=True).aggregate(avg=Avg('rating'), count=Count('id'))
        self.avg_rating = stats['avg'] or 0.00
        self.review_count = stats['count']
        self.save(update_fields=['avg_rating', 'review_count'])


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Sản phẩm')
    image = models.ImageField(upload_to='products/', verbose_name='Hình ảnh')
    is_primary = models.BooleanField(default=False, verbose_name='Ảnh chính')
    display_order = models.IntegerField(default=0, verbose_name='Thứ tự')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'product_images'
        verbose_name = 'Hình ảnh sản phẩm'
        verbose_name_plural = 'Hình ảnh sản phẩm'
        ordering = ['display_order', 'created_at']
    
    def __str__(self):
        return f"{self.product.name} - Image {self.id}"
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).exclude(id=self.id).update(is_primary=False)
        super().save(*args, **kwargs)
