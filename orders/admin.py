from django.contrib import admin
from .models import Order, OrderItem, Cart


class OrderItemInline(admin.TabularInline):
    """Inline for order items"""
    model = OrderItem
    extra = 0
    fields = ['product', 'product_name', 'price', 'quantity', 'subtotal']
    readonly_fields = ['product_name', 'price', 'subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order admin"""
    
    list_display = [
        'order_number', 'user', 'customer_name', 'total_amount',
        'status', 'payment_method', 'ordered_at'
    ]
    list_filter = ['status', 'payment_method', 'ordered_at']
    search_fields = ['order_number', 'customer_name', 'customer_phone']
    readonly_fields = [
        'order_number', 'subtotal', 'total_amount',
        'ordered_at', 'confirmed_at', 'shipped_at', 'completed_at', 'cancelled_at'
    ]
    ordering = ['-ordered_at']
    
    fieldsets = (
        ('Thông tin đơn hàng', {
            'fields': ('order_number', 'user', 'status', 'payment_method', 'payment_status')
        }),
        ('Thông tin khách hàng', {
            'fields': ('customer_name', 'customer_phone', 'customer_email', 'shipping_address', 'note')
        }),
        ('Tài chính', {
            'fields': ('subtotal', 'shipping_fee', 'discount', 'total_amount')
        }),
        ('Thời gian', {
            'fields': ('ordered_at', 'confirmed_at', 'shipped_at', 'completed_at', 'cancelled_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [OrderItemInline]
    
    actions = ['mark_as_processing', 'mark_as_shipping', 'mark_as_completed']
    
    def mark_as_processing(self, request, queryset):
        for order in queryset:
            order.update_status('processing')
        self.message_user(request, f'{queryset.count()} đơn hàng đã chuyển sang trạng thái Đang xử lý.')
    mark_as_processing.short_description = 'Đánh dấu: Đang xử lý'
    
    def mark_as_shipping(self, request, queryset):
        for order in queryset:
            order.update_status('shipping')
        self.message_user(request, f'{queryset.count()} đơn hàng đã chuyển sang trạng thái Đang giao hàng.')
    mark_as_shipping.short_description = 'Đánh dấu: Đang giao hàng'
    
    def mark_as_completed(self, request, queryset):
        for order in queryset:
            order.update_status('completed')
        self.message_user(request, f'{queryset.count()} đơn hàng đã hoàn thành.')
    mark_as_completed.short_description = 'Đánh dấu: Hoàn thành'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Cart admin"""
    
    list_display = ['user', 'product', 'quantity', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__email', 'product__name']
    ordering = ['-added_at']
