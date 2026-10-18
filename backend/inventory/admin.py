
from django.contrib import admin

from .models import (
    Category,
    Supplier,
    Customer,
    Product,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "name",
        "category",
        "cost_price",
        "selling_price",
        "stock_quantity",
        "reorder_level",
        "is_active",
    )

    search_fields = ("sku", "name")
    list_filter = ("category", "is_active")
    list_per_page = 20

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email")
    search_fields = ("name", "phone", "email")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email")
    search_fields = ("name", "phone", "email")
