from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('offers/', views.offers, name='offers'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('track-order/', views.track_order, name='track_order'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),

    # Payment
    path('payment/create-order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('payment/verify/', views.payment_verify, name='payment_verify'),
    path('payment/success/<str:order_id>/', views.payment_success, name='payment_success'),

    # Cart actions
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),

    # Wishlist actions
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
]
