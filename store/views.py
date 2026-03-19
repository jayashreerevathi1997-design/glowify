import uuid
import razorpay
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from .models import (
    Category, Product, Ingredient,
    Cart, CartItem, Wishlist, WishlistItem,
    Order, OrderItem
)

# Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def get_or_create_cart(request):
    """Get or create a cart for the current session."""
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def get_or_create_wishlist(request):
    """Get or create a wishlist for the current session."""
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    wishlist, created = Wishlist.objects.get_or_create(session_key=session_key)
    return wishlist


def home(request):
    """Home page view."""
    featured_products = Product.objects.filter(is_featured=True).select_related('category')[:6]
    categories = Category.objects.all()
    ingredients = Ingredient.objects.all()

    wishlist_product_ids = []
    if request.session.session_key:
        try:
            wishlist = Wishlist.objects.get(session_key=request.session.session_key)
            wishlist_product_ids = list(wishlist.items.values_list('product_id', flat=True))
        except Wishlist.DoesNotExist:
            pass

    context = {
        'featured_products': featured_products,
        'categories': categories,
        'ingredients': ingredients,
        'wishlist_product_ids': wishlist_product_ids,
        'fallback_categories': ['Lipstick', 'Serum', 'Foundation', 'Blush', 'Lip Gloss', 'Mist'],
    }
    return render(request, 'home.html', context)


def shop(request):
    """Shop page view with filtering."""
    products = Product.objects.all().select_related('category')
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    sort_by = request.GET.get('sort', 'default')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')

    wishlist_product_ids = []
    if request.session.session_key:
        try:
            wishlist = Wishlist.objects.get(session_key=request.session.session_key)
            wishlist_product_ids = list(wishlist.items.values_list('product_id', flat=True))
        except Wishlist.DoesNotExist:
            pass

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'sort_by': sort_by,
        'wishlist_product_ids': wishlist_product_ids,
    }
    return render(request, 'store/shop.html', context)


def product_detail(request, slug):
    """Product detail view."""
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    in_wishlist = False
    if request.session.session_key:
        try:
            wishlist = Wishlist.objects.get(session_key=request.session.session_key)
            in_wishlist = wishlist.items.filter(product=product).exists()
        except Wishlist.DoesNotExist:
            pass

    context = {
        'product': product,
        'related_products': related_products,
        'in_wishlist': in_wishlist,
        'star_range': range(int(product.rating)),
        'empty_star_range': range(5 - int(product.rating)),
    }
    return render(request, 'store/product_detail.html', context)


@require_POST
def add_to_cart(request, product_id):
    """Add a product to the cart via AJAX."""
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return JsonResponse({
        'success': True,
        'message': f'{product.name} added to cart!',
        'cart_count': cart.item_count,
    })


@require_POST
def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    cart = get_or_create_cart(request)
    try:
        item = CartItem.objects.get(id=item_id, cart=cart)
        item.delete()
        messages.success(request, 'Item removed from cart.')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found in cart.')
    return redirect('cart')


@require_POST
def update_cart(request, item_id):
    """Update cart item quantity via AJAX."""
    cart = get_or_create_cart(request)
    try:
        item = CartItem.objects.get(id=item_id, cart=cart)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count,
            'cart_total': float(cart.total),
            'item_subtotal': float(item.subtotal) if quantity > 0 else 0,
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Item not found.'})


def cart(request):
    """Cart page view."""
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)


@require_POST
def toggle_wishlist(request, product_id):
    """Toggle a product in/out of the wishlist via AJAX."""
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_or_create_wishlist(request)

    wishlist_item = WishlistItem.objects.filter(wishlist=wishlist, product=product).first()
    if wishlist_item:
        wishlist_item.delete()
        in_wishlist = False
        message = f'{product.name} removed from wishlist.'
    else:
        WishlistItem.objects.create(wishlist=wishlist, product=product)
        in_wishlist = True
        message = f'{product.name} added to wishlist!'

    return JsonResponse({
        'success': True,
        'in_wishlist': in_wishlist,
        'message': message,
        'wishlist_count': wishlist.item_count,
    })


def wishlist(request):
    """Wishlist page view."""
    wishlist = get_or_create_wishlist(request)
    wishlist_items = wishlist.items.select_related('product').all()

    context = {
        'wishlist': wishlist,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'store/wishlist.html', context)


def about(request):
    """About page view."""
    return render(request, 'store/about.html')


def contact(request):
    """Contact page view."""
    return render(request, 'store/contact.html')


def offers(request):
    """Offers page view."""
    products = Product.objects.filter(badge__in=['Best Seller', 'Hot Pick', 'Trending'])
    context = {'products': products}
    return render(request, 'store/offers.html', context)


def checkout(request):
    """Checkout page view."""
    cart_obj = get_or_create_cart(request)
    cart_items = cart_obj.items.select_related('product').all()

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('shop')

    context = {
        'cart': cart_obj,
        'cart_items': cart_items,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
    }
    return render(request, 'store/checkout.html', context)


@require_POST
def create_razorpay_order(request):
    """AJAX: Create order in DB + Razorpay and return order details."""
    cart_obj = get_or_create_cart(request)
    cart_items = cart_obj.items.select_related('product').all()

    if not cart_items.exists():
        return JsonResponse({'success': False, 'message': 'Cart is empty.'})

    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    mobile = request.POST.get('mobile', '')
    address = request.POST.get('address', '')
    city = request.POST.get('city', '')
    state = request.POST.get('state', '')
    pincode = request.POST.get('pincode', '')
    shipping_method = request.POST.get('shipping', 'standard')

    subtotal = cart_obj.total
    shipping = 50 if shipping_method == 'standard' else 100
    total = subtotal + shipping

    # Create order in DB
    order_id = f"GLOW-{uuid.uuid4().hex[:8].upper()}"
    order = Order.objects.create(
        order_id=order_id,
        session_key=request.session.session_key,
        first_name=first_name,
        last_name=last_name,
        mobile=mobile,
        address=address,
        city=city,
        state=state,
        pincode=pincode,
        subtotal=subtotal,
        shipping=shipping,
        total=total,
        status='created',
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity,
        )

    # Create Razorpay order
    razorpay_order = razorpay_client.order.create({
        'amount': int(total * 100),
        'currency': 'INR',
        'receipt': order_id,
        'payment_capture': 1,
    })

    order.razorpay_order_id = razorpay_order['id']
    order.save()

    return JsonResponse({
        'success': True,
        'order_id': order_id,
        'razorpay_order_id': razorpay_order['id'],
        'amount': int(total * 100),
        'name': f'{first_name} {last_name}',
        'mobile': mobile,
    })


@require_POST
def payment_verify(request):
    """AJAX: Verify Razorpay payment signature."""
    razorpay_order_id = request.POST.get('razorpay_order_id', '')
    razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
    razorpay_signature = request.POST.get('razorpay_signature', '')

    if not razorpay_order_id or not razorpay_payment_id:
        return JsonResponse({'success': False, 'message': 'Payment data missing.'})

    try:
        order = Order.objects.get(razorpay_order_id=razorpay_order_id)
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Order not found.'})

    order.razorpay_payment_id = razorpay_payment_id
    order.razorpay_signature = razorpay_signature

    try:
        razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature,
        })
        order.status = 'paid'
        order.save()

        # Clear the cart
        cart_obj = get_or_create_cart(request)
        cart_obj.items.all().delete()

        return JsonResponse({
            'success': True,
            'redirect_url': f'/payment/success/{order.order_id}/',
        })

    except Exception:
        order.status = 'failed'
        order.save()
        return JsonResponse({'success': False, 'message': 'Payment verification failed.'})


def payment_success(request, order_id):
    """Payment success page."""
    order = get_object_or_404(Order, order_id=order_id, status='paid')
    order_items = order.items.select_related('product').all()

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'store/order_confirmation.html', context)


def order_confirmation(request):
    """Order confirmation page view (legacy)."""
    cart_obj = get_or_create_cart(request)
    cart_items = cart_obj.items.select_related('product').all()
    context = {
        'cart': cart_obj,
        'cart_items': cart_items,
    }
    return render(request, 'store/order_confirmation.html', context)


def login_view(request):
    """Login page view."""
    return render(request, 'store/login.html')


def signup_view(request):
    """Signup page view."""
    return render(request, 'store/signup.html')


def track_order(request):
    """Track order page view."""
    steps1 = [
        (1, 'Ordered', True),
        (2, 'Processing', True),
        (3, 'Shipped', True),
        (4, 'Out for Delivery', False),
    ]
    steps2 = [
        (1, 'Ordered', True),
        (2, 'Processing', True),
        (3, 'Shipped', False),
        (4, 'Out for Delivery', False),
    ]
    context = {
        'steps1': steps1,
        'steps2': steps2,
    }
    return render(request, 'store/track_order.html', context)
