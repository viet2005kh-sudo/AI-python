from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    """Inline for product images"""
    model = ProductImage
    extra = 1
    fields = ['image', 'is_primary', 'display_order']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin"""
    
    list_display = ['name', 'slug', 'icon', 'is_active', 'display_order', 'get_products_count']
    list_filter = ['is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['display_order', 'name']
    
    def get_products_count(self, obj):
        return obj.get_products_count()
    get_products_count.short_description = 'Số sản phẩm'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product admin"""
    
    list_display = [
        'name', 'category', 'price', 'discount_price', 'stock_quantity',
        'sold_count', 'is_featured', 'is_active', 'created_at'
    ]
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock_quantity', 'is_featured', 'is_active']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Giá & Kho', {
            'fields': ('price', 'discount_price', 'stock_quantity', 'unit', 'weight_grams')
        }),
        ('Thống kê', {
            'fields': ('sold_count', 'view_count', 'avg_rating', 'review_count'),
            'classes': ('collapse',)
        }),
        ('Trạng thái', {
            'fields': ('is_featured', 'is_active')
        }),
    )
    
    readonly_fields = ['sold_count', 'view_count', 'avg_rating', 'review_count']
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Product image admin"""
    
    list_display = ['product', 'is_primary', 'display_order', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name']

