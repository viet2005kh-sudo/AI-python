# reviews/admin.py

from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review admin"""
    
    list_display = [
        'user', 'product', 'rating', 'is_verified_purchase',
        'is_approved', 'helpful_count', 'created_at'
    ]
    list_filter = ['rating', 'is_verified_purchase', 'is_approved', 'created_at']
    search_fields = ['user__full_name', 'product__name', 'title', 'content']
    list_editable = ['is_approved']
    readonly_fields = ['helpful_count', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('user', 'product', 'rating')
        }),
        ('Nội dung', {
            'fields': ('title', 'content', 'image')
        }),
        ('Trạng thái', {
            'fields': ('is_verified_purchase', 'is_approved', 'helpful_count')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} đánh giá đã được duyệt.')
    approve_reviews.short_description = 'Duyệt đánh giá'
    
    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} đánh giá đã bị từ chối.')
    disapprove_reviews.short_description = 'Từ chối đánh giá'