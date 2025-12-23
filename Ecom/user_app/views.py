from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from admin_app.models import OrderItem, Order

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'user_app/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            next_url = request.GET.get('next') or 'dashboard'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'user_app/login.html')

def logout_view(request):
    request.session.flush()
    logout(request)
    messages.info(request, 'You have logged out successfully.')
    return redirect('home')

@login_required
def dashboard(request):
    user = request.user

    # User orders
    orders = OrderItem.objects.filter(order__user=request.user)
    total_orders = orders.count()

    # Order items belonging to user's orders
    order_items = OrderItem.objects.filter(
        order__user=user
    ).select_related('product', 'order')

    total_amount = sum(
        item.product.price * item.quantity
        for item in order_items
    )

    context = {
        "user": user,
        "orders": orders[:5],          # last 5 orders
        "order_items": order_items,    # ALL ordered items
        "total_orders": total_orders,
        "total_amount": total_amount,
    }

    return render(request, "user_app/dashboard.html", context)
