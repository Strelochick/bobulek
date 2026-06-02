from django.contrib import admin

from .models import Category, Customer, Manufacturer, Order, OrderItem, Product, Promotion, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'address')
    search_fields = ('name', 'phone', 'address')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'manufacturer', 'price', 'weight', 'is_available', 'created_at')
    list_filter = ('category', 'manufacturer', 'is_available', 'created_at')
    search_fields = ('name', 'short_description', 'composition')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'email', 'address')
    search_fields = ('first_name', 'last_name', 'phone', 'email')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'customer__first_name', 'customer__last_name')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    list_filter = ('order', 'product')
    search_fields = ('product__name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'customer_name', 'text')


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'discount_percent', 'start_date', 'end_date')
    list_filter = ('discount_percent', 'start_date', 'end_date')
    search_fields = ('title', 'description')
