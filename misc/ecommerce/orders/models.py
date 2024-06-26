import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

def generate_order_id():
    timestamp = timezone.now().strftime("%y%m%d")
    unique_id = uuid.uuid4().hex[:6]  # Generate a random 8-character string
    # yymm + unique_id upper
    return f"{timestamp}{unique_id.upper()}"

class Order(models.Model):
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order_id = models.CharField(max_length=220, default=generate_order_id)
    user = models.ForeignKey("web.User", on_delete=models.CASCADE, null=True, blank=True)
    payable = models.DecimalField(max_digits=10, decimal_places=2)
    completed_at = models.DateTimeField(blank=True, null=True)

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    address_line_1 = models.CharField("Address 1", max_length=100, blank=True, null=True)
    address_line_2 = models.CharField("Address 2", max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    alternate_mobile = models.CharField(max_length=15, blank=True, null=True)
    email= models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=100,
        default="Pending",
        choices=(
            ("Pending", "Pending"),
            ("Shipped", "Order Shipped"),
            ("Delivered", "Order Delivered"),
            ("Cancelled", "Order Cancelled"),
        ),
    )

    def get_items(self):
        return OrderItem.objects.filter(order=self)

    def get_items_count(self):
        return self.get_items().count()

    def total(self):
        return sum([item.subtotal() for item in self.get_items()])

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return f"{self.order_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_option = models.ForeignKey("web.ProductVariant", related_name="order_items",on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1,)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.product_option} - {self.quantity}"

    def subtotal(self):
        return self.price * self.quantity