"""
Views for user authentication and account management
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import User


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Xin chào {user.full_name}!')
                    
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    elif user.is_admin:
                        return redirect('core:admin_dashboard')
                    else:
                        return redirect('core:home')
                else:
                    messages.error(request, 'Tài khoản đã bị khóa.')
            else:
                messages.error(request, 'Email hoặc mật khẩu không đúng.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'Đã đăng xuất thành công.')
    return redirect('core:home')


@login_required
def profile_view(request):
    """User profile view"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thông tin thành công!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    total_orders = request.user.get_total_orders()
    total_spent = request.user.get_total_spent()
    
    context = {
        'form': form,
        'total_orders': total_orders,
        'total_spent': total_spent,
    }
    
    return render(request, 'accounts/profile.html', context)


@login_required
def order_history_view(request):
    """User order history view"""
    orders = request.user.orders.all()
    
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    context = {
        'orders': orders,
        'current_status': status,
    }
    
    return render(request, 'accounts/order_history.html', context)
