
from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem, Transaction
from .utils import send_order_status_email
from django.db import transaction


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'user',
        'status',
        'total_amount',
        'estimated_delivery',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'order_number',
        'user__username',
        'shipping_full_name',
    )

    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        old_status = None

        if change:
            old_status = Order.objects.get(pk=obj.pk).status

        super().save_model(request, obj, form, change)

        if change and old_status != obj.status:
            transaction.on_commit(
                lambda: send_order_status_email(obj)
            )


admin.site.register(ShippingAddress)
admin.site.register(OrderItem)
admin.site.register(Transaction)
