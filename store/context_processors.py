from .models import Cart, Wishlist


def cart_wishlist_count(request):
    """Add cart and wishlist counts to all template contexts."""
    cart_count = 0
    wishlist_count = 0

    if request.session.session_key:
        try:
            cart = Cart.objects.get(session_key=request.session.session_key)
            cart_count = cart.item_count
        except Cart.DoesNotExist:
            pass

        try:
            wishlist = Wishlist.objects.get(session_key=request.session.session_key)
            wishlist_count = wishlist.item_count
        except Wishlist.DoesNotExist:
            pass

    return {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
    }
