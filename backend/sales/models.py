
from django.conf import settings
from django.db import models
from django.db.models import Q


class Sale(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    customer = models.ForeignKey(
        "inventory.Customer",
        on_delete=models.PROTECT,
        related_name="sales",
        null=True,
        blank=True,
    )

    sold_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )

    date = models.DateTimeField(auto_now_add=True)

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.CheckConstraint(
                condition=Q(total_amount__gte=0),
                name="sale_total_nonnegative",
            ),
        ]

    def __str__(self):
        return f"Sale #{self.id} - {self.status}"


class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        "inventory.Product",
        on_delete=models.PROTECT,
        related_name="sale_items",
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    subtotal = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gt=0),
                name="sale_item_quantity_positive",
            ),
            models.CheckConstraint(
                condition=Q(unit_price__gte=0),
                name="sale_item_price_nonnegative",
            ),
            models.CheckConstraint(
                condition=Q(discount__gte=0),
                name="sale_item_discount_nonnegative",
            ),
            models.CheckConstraint(
                condition=Q(subtotal__gte=0),
                name="sale_item_subtotal_nonnegative",
            ),
            models.UniqueConstraint(
                fields=["sale", "product"],
                name="unique_product_per_sale",
            ),
        ]

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class SalesReturn(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.PROTECT,
        related_name="returns",
    )

    returned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )

    date = models.DateTimeField(auto_now_add=True)

    total_refund = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.CheckConstraint(
                condition=Q(total_refund__gte=0),
                name="sales_return_refund_nonnegative",
            ),
        ]

    def __str__(self):
        return f"Return #{self.id} - Sale #{self.sale_id}"


class SalesReturnItem(models.Model):
    sales_return = models.ForeignKey(
        SalesReturn,
        on_delete=models.CASCADE,
        related_name="items",
        db_column="return_id",
    )

    sale_item = models.ForeignKey(
        SaleItem,
        on_delete=models.PROTECT,
        related_name="return_items",
    )

    quantity = models.PositiveIntegerField()

    refund_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    restock = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gt=0),
                name="sales_return_item_quantity_positive",
            ),
            models.CheckConstraint(
                condition=Q(refund_amount__gte=0),
                name="sales_return_item_refund_nonnegative",
            ),
            models.UniqueConstraint(
                fields=["sales_return", "sale_item"],
                name="unique_sale_item_per_return",
            ),
        ]

    def __str__(self):
        return f"Return item #{self.id} - Qty {self.quantity}"
