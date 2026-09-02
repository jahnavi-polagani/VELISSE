from django.contrib import admin

from .models import (
    Product,
    Order,
    OrderItem,
    ContactMessage
)


# =========================
# PRODUCT ADMIN
# =========================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
        'price',
        'stock',
    )

    list_filter = (
        'category',
    )

    search_fields = (
        'name',
        'description',
    )

    ordering = (
        'name',
    )


# =========================
# ORDER ITEM INLINE
# =========================

class OrderItemInline(
    admin.TabularInline
):

    model = OrderItem

    extra = 0

    fields = (
        'product',
        'quantity',
        'size',
        'price',
    )


# =========================
# ORDER ADMIN
# =========================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'customer_name',
        'email',
        'phone',
        'total_price',
        'created_at',
    )

    search_fields = (
        'customer_name',
        'email',
        'phone',
    )

    list_filter = (
        'created_at',
    )

    ordering = (
        '-created_at',
    )

    inlines = (
        OrderItemInline,
    )


# =========================
# CONTACT MESSAGE ADMIN
# =========================

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'created_at',
    )

    search_fields = (
        'name',
        'email',
        'message',
    )

    ordering = (
        '-created_at',
    )