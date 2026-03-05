from django import forms
from django.core.exceptions import ValidationError
from .models import User


class UserRegistrationForm(forms.ModelForm):
    """User registration form"""
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mật khẩu (tối thiểu 8 ký tự)'
        }),
        label='Mật khẩu'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Xác nhận mật khẩu'
        }),
        label='Xác nhận mật khẩu'
    )
    
    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email của bạn'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Họ và tên'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Số điện thoại'
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email này đã được sử dụng.')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise ValidationError('Số điện thoại chỉ được chứa số.')
        if phone and len(phone) != 10:
            raise ValidationError('Số điện thoại phải có 10 số.')
        return phone
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError('Mật khẩu không khớp.')
            
            if len(password) < 8:
                raise ValidationError('Mật khẩu phải có ít nhất 8 ký tự.')
        
        return cleaned_data


class UserLoginForm(forms.Form):
    """User login form"""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email của bạn'
        }),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mật khẩu'
        }),
        label='Mật khẩu'
    )


class UserProfileForm(forms.ModelForm):
    """User profile update form"""
    
    class Meta:
        model = User
        fields = ['full_name', 'phone', 'address', 'avatar']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Họ và tên'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Số điện thoại'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Địa chỉ chi tiết',
                'rows': 3
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise ValidationError('Số điện thoại chỉ được chứa số.')
        if phone and len(phone) != 10:
            raise ValidationError('Số điện thoại phải có 10 số.')
        return phone
    
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Check file size (max 5MB)
            if avatar.size > 5 * 1024 * 1024:
                raise ValidationError('Kích thước ảnh không được vượt quá 5MB.')
            
            # Check file extension
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            ext = avatar.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise ValidationError('Chỉ chấp nhận file ảnh: jpg, jpeg, png, gif.')
        
        return avatar