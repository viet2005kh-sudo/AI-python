# reviews/forms.py - Review form

from django import forms
from reviews.models import Review


class ReviewForm(forms.ModelForm):
    """Product review form"""
    
    class Meta:
        model = Review
        fields = ['rating', 'title', 'content', 'image']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} ★') for i in range(1, 6)]),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tóm tắt đánh giá của bạn'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Chia sẻ trải nghiệm của bạn về sản phẩm này...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'rating': 'Đánh giá',
            'title': 'Tiêu đề',
            'content': 'Nội dung',
            'image': 'Hình ảnh (tùy chọn)',
        }