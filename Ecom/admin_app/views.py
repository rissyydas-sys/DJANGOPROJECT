from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, Profile
from django.contrib import messages

def product_list(request):
    products = Product.objects.all()
    return render(request, 'admin_app/products.html', {'products': products})


def home(request):
    return render(request, 'admin_app/home.html')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Recently viewed session
    viewed = request.session.get('viewed_products', [])
    if pk not in viewed:
        viewed.append(pk)
        request.session['viewed_products'] = viewed

    return render(request, 'admin_app/product_detail.html', {'product': product})


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = Product.objects.get(id=product_id)

    pid = str(product_id)

    if pid in cart and isinstance(cart[pid], dict):
        cart[pid]['quantity'] += 1
    else:
        cart[pid] = {
            'price': float(product.price),
            'quantity': 1
        }

    request.session['cart'] = cart
    return redirect('view_cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        del cart[pid]

    request.session['cart'] = cart   # ✅ HERE
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        raw_item = cart.get(str(product.id))

        # 🔒 SAFETY CHECK
        if isinstance(raw_item, int):
            quantity = raw_item
            price = float(product.price)
        else:
            quantity = raw_item.get('quantity', 0)
            price = raw_item.get('price', float(product.price))

        subtotal = quantity * price
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'price': price,
            'subtotal': subtotal,
        })

    return render(request, 'admin_app/cart.html', {
        'cart_items': cart_items,
        'total': total
    })




@login_required
def place_order(request):
    cart = request.session.get('cart', {})

    # If cart is empty, do nothing
    if not cart:
        return redirect('view_cart')

    # Create order
    order = Order.objects.create(
        user=request.user,
        status='Pending'
    )

    # Create order items
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )

        # Optional: reduce stock
        product.stock -= quantity
        product.save()

    # Clear cart after placing order
    request.session['cart'] = {}

    messages.success(request, "✅ Order placed successfully!")

    return redirect('view_cart') 

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')

    order = Order.objects.create(user=request.user)

    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        OrderItem.objects.create(order=order, product=product, quantity=qty)

    request.session['cart'] = {}
    return redirect('order_history')


@login_required
def order_history(request):
    # orders = Order.objects.filter(user=request.user)
    orders = OrderItem.objects.filter(order__user=request.user)
    return render(request, 'admin_app/orders.html', {'orders': orders})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.phone = request.POST['phone']
        profile.address = request.POST['address']
        profile.save()

    return render(request, 'shop/profile.html', {'profile': profile})

def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)

    qty = int(request.POST.get('quantity'))

    if qty > 0:
        cart[pid]['quantity'] = qty
    else:
        del cart[pid]

    request.session['cart'] = cart  
    return redirect('view_cart')

@login_required
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.save()
        return redirect('dashboard')

    return render(request, 'admin_app/update_profile.html', {
        'profile': profile
    })

@login_required
def view_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    return render(request, 'admin_app/view_profile.html', {
        'profile': profile
    })