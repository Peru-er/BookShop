
import uuid

from django.db import models
from django.contrib.auth.models import User
from cart.models import Cart
from shop.models import Product
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField('Full name', max_length=200)
    phone = models.CharField('Phone', max_length=20)
    country = models.CharField('Country', max_length=100, default='England')
    city = models.CharField('City', max_length=100)
    postal_code = models.CharField('Zip code', max_length=20)
    address_line1 = models.CharField('Address (line 1)', max_length=250)
    address_line2 = models.CharField('Address (line 2)', max_length=250, blank=True)
    is_default = models.BooleanField('By default', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Delivery address'
        verbose_name_plural = 'Deliveries addresses'
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.city}"

    def save(self, *args, **kwargs):
        if self.is_default:
            ShippingAddress.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class Transaction(models.Model):
    reference = models.CharField(max_length=255)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    shipping_full_name = models.CharField(max_length=200)
    shipping_phone = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    shipping_city = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_address_line1 = models.CharField(max_length=250)
    shipping_address_line2 = models.CharField(max_length=250, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    estimated_delivery = models.DateField(
        blank=True,
        null=True,
    )

    @property
    def can_cancel(self):
        return (
                self.status == self.Status.PENDING
                and timezone.now() <= self.created_at + timedelta(hours=24)
        )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.price * self.quantity


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=50)
    note = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(pre_save, sender=Order)
def restore_stock_on_cancelled(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_order = Order.objects.get(pk=instance.pk)
            if old_order.status != 'cancelled' and instance.status == 'cancelled':

                items = OrderItem.objects.filter(order=instance)

                for item in items:
                    if item.product:
                        product = item.product
                        product.stock += item.quantity
                        if product.stock > 0:
                            product.is_available = True
                        product.save()

        except Order.DoesNotExist:
            pass
