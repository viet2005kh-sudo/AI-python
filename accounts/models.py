"""
Models for user accounts and authentication
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom manager for User model"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user"""
        if not email:
            raise ValueError('Email là bắt buộc')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser phải có is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser phải có is_superuser=True')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model with email as username"""
    
    ROLE_CHOICES = (
        ('user', 'Người dùng'),
        ('admin', 'Quản trị viên'),
    )
    
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=100, verbose_name='Họ tên')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Số điện thoại')
    address = models.TextField(blank=True, verbose_name='Địa chỉ')
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True,
        verbose_name='Ảnh đại diện'
    )
    
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='user',
        verbose_name='Vai trò'
    )
    
    is_active = models.BooleanField(default=True, verbose_name='Kích hoạt')
    is_staff = models.BooleanField(default=False, verbose_name='Nhân viên')
    email_verified = models.BooleanField(default=False, verbose_name='Email đã xác thực')
    
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Ngày tham gia')
    last_login = models.DateTimeField(null=True, blank=True, verbose_name='Đăng nhập cuối')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Người dùng'
        verbose_name_plural = 'Người dùng'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.full_name
    
    def get_short_name(self):
        return self.full_name.split()[0] if self.full_name else self.email
    
    @property
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin' or self.is_superuser
    
    def get_total_orders(self):
        """Get total orders count"""
        return self.orders.count()
    
    def get_total_spent(self):
        """Get total amount spent"""
        from django.db.models import Sum
        total = self.orders.filter(
            status='completed'
        ).aggregate(
            total=Sum('total_amount')
        )['total']
        return total or 0