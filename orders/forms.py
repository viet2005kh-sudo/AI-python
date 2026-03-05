from django import forms
from .models import Order


class CheckoutForm(forms.Form):
    """Checkout form"""
    
    customer_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Họ và tên'
        }),
        label='Họ tên người nhận'
    )
    
    customer_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0901234567'
        }),
        label='Số điện thoại'
    )
    
    customer_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com'
        }),
        label='Email (tùy chọn)'
    )
    
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Số nhà, tên đường, phường/xã, quận/huyện, tỉnh/thành phố',
            'rows': 3
        }),
        label='Địa chỉ giao hàng'
    )
    
    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ghi chú cho đơn hàng (tùy chọn)',
            'rows': 2
        }),
        label='Ghi chú'
    )
    
    payment_method = forms.ChoiceField(
        choices=Order.PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect,
        label='Phương thức thanh toán',
        initial='cod'
    )
    
    def clean_customer_phone(self):
        phone = self.cleaned_data.get('customer_phone')
        if not phone.isdigit():
            raise forms.ValidationError('Số điện thoại chỉ được chứa số.')
        if len(phone) != 10:
            raise forms.ValidationError('Số điện thoại phải có 10 số.')
        return phone