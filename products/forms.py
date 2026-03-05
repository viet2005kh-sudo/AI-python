from django import forms
from django.forms import inlineformset_factory
from products.models import Product, ProductImage, Category


class ProductForm(forms.ModelForm):
    """Product form for admin"""
    
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'description', 'price', 'discount_price',
            'stock_quantity', 'unit', 'weight_grams', 'is_featured', 'is_active'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tên sản phẩm'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Mô tả chi tiết sản phẩm'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'discount_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0 (để trống nếu không có giảm giá)'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'gói, hộp, kg...'
            }),
            'weight_grams': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Khối lượng (gram)'
            }),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        discount_price = cleaned_data.get('discount_price')
        
        if discount_price and price:
            if discount_price >= price:
                raise forms.ValidationError(
                    'Giá khuyến mãi phải nhỏ hơn giá gốc.'
                )
        
        return cleaned_data


class ProductImageForm(forms.ModelForm):
    """Product image form"""
    
    class Meta:
        model = ProductImage
        fields = ['image', 'is_primary', 'display_order']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Kích thước ảnh không được vượt quá 5MB.')
            
            # Check file extension
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            ext = image.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError(
                    'Chỉ chấp nhận file ảnh: jpg, jpeg, png, gif, webp.'
                )
        
        return image


# Formset for managing multiple product images
ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=3,  # Number of empty forms to display
    can_delete=True
)


class CategoryForm(forms.ModelForm):
    """Category form for admin"""
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'icon', 'image', 'is_active', 'display_order']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tên danh mục'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Mô tả danh mục'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emoji hoặc icon class (🍪, fa-cookie...)'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
        }