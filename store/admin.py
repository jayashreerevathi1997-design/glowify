from django.contrib import admin
from .models import Category, Product, Ingredient, Cart, CartItem, Wishlist, WishlistItem, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'badge', 'rating', 'review_count', 'is_featured', 'stock']
    list_filter = ['category', 'badge', 'is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'is_featured', 'stock']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'benefit']
    search_fields = ['name']


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'item_count', 'total', 'created_at']
    inlines = [CartItemInline]


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'item_count', 'created_at']
    inlines = [WishlistItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'first_name', 'mobile', 'total', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['order_id', 'first_name', 'razorpay_payment_id']
    inlines = [OrderItemInline]


admin.site.site_header = 'Glowify Admin'
admin.site.site_title = 'Glowify'
admin.site.index_title = 'Welcome to Glowify Administration'
