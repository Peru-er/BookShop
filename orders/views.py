from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Max
from django_ratelimit.decorators import ratelimit

from datetime import timedelta
from django.utils import timezone

from cart.cart import get_cart
from shop.models import Product
from .models import Order, OrderItem, ShippingAddress, OrderStatusHistory
from .forms import ShippingAddressForm, OrderCheckoutForm
from .utils import send_order_status_email, send_order_confirmation_email


@login_required
def checkout(request):
    cart = get_cart(request)

    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('shop:catalog')

    addresses = ShippingAddress.objects.filter(user=request.user)

    if request.method == 'POST':
        if 'select_address' in request.POST:
            address_id = request.POST.get('address_id')
            request.session['shipping_address_id'] = address_id
            return redirect('orders:checkout_confirm')

        elif 'add_new_address' in request.POST:
            form = ShippingAddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                address.user = request.user
                address.save()

                request.session['shipping_address_id'] = address.id
                messages.success(request, 'Address added successfully')
                return redirect('orders:checkout_confirm')
    else:
        form = ShippingAddressForm()

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'addresses': addresses,
        'form': form,
    })


@login_required
@ratelimit(key='user', rate='5/m', block=True)
def checkout_confirm(request):
    cart = get_cart(request)

    address_id = request.session.get('shipping_address_id')
    if not address_id:
        messages.warning(request, 'Please select a delivery address')
        return redirect('orders:checkout')

    address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)

    if request.method == 'POST':
        form = OrderCheckoutForm(request.POST)
        if form.is_valid():
            order = create_order(
                request=request,
                cart=cart,
                address=address,
                payment_method=form.cleaned_data['payment_method'],
                notes=form.cleaned_data['notes']
            )

            if order:
                send_order_confirmation_email(order)
                cart.clear()
                if 'shipping_address_id' in request.session:
                    del request.session['shipping_address_id']

                messages.success(request, f'Order #{order.order_number} created successfully.')
                return redirect('orders:order_success', order_number=order.order_number)
            else:
                messages.error(request, 'Error creating order')
    else:
        form = OrderCheckoutForm()

    return render(request, 'orders/checkout_confirm.html', {
        'cart': cart,
        'address': address,
        'form': form,
    })


@transaction.atomic
def create_order(request, cart, address, payment_method, notes):
    try:
        order = Order.objects.create(
            user=request.user,
            shipping_full_name=address.full_name,
            shipping_phone=address.phone,
            shipping_country=address.country,
            shipping_city=address.city,
            shipping_postal_code=address.postal_code,
            shipping_address_line1=address.address_line1,
            shipping_address_line2=address.address_line2,
            total_amount=cart.get_total_price(),
            notes=notes
        )

        order.estimated_delivery = timezone.now().date() + timedelta(days=5)
        order.save()

        for item in cart:
            product = Product.objects.select_for_update().get(id=item['product'].id)
            quantity_requested = item['quantity']

            if product.stock < quantity_requested:
                raise ValueError(f"Sorry, only {product.stock} units of '{product.name}' are available.")

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                price=product.price,
                quantity=quantity_requested
            )

            product.stock -= quantity_requested

            if product.stock == 0:
                product.is_available = False

            product.save()

        OrderStatusHistory.objects.create(
            order=order,
            status='pending',
            note=f'Order created. Payment method: {payment_method}',
            created_by=request.user
        )

        return order

    except ValueError as e:
        transaction.set_rollback(True)
        messages.error(request, str(e))
        return None

    except Exception as e:
        transaction.set_rollback(True)
        messages.error(request, f'Error: {str(e)}')
        return None


@login_required
def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_list(request):
    active_orders = Order.objects.filter(
        user=request.user
    ).prefetch_related('items__product').exclude(
        status__in=['delivered', 'cancelled']
    ).order_by('-created_at')

    return render(request, 'users:profile', {
        'active_orders': active_orders
    })


@login_required
def order_history(request):
    archived_orders = Order.objects.filter(
        user=request.user
    ).prefetch_related('items__product').filter(
        status__in=['delivered', 'cancelled']
    ).annotate(
        last_status_update=Max('status_history__created_at')
    ).order_by('-last_status_update')

    return render(request, 'orders/order_history.html', {
        'archived_orders': archived_orders
    })


@login_required
def order_detail(request, order_number):

    order = get_object_or_404(
        Order.objects.select_related('user').prefetch_related(
            'items__product',
            'status_history'
        ),
        order_number=order_number,
        user=request.user
    )

    return render(request, 'orders/order_detail.html', {
        'order': order
    })


@login_required
@transaction.atomic
def cancel_order(request, order_id):
    if request.method != 'POST':
        return redirect('users:profile')

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if not order.can_cancel:
        messages.error(
            request,
            'This order can no longer be cancelled.'
        )
        return redirect('users:profile')

    for item in order.items.all():
        if item.product:
            product = Product.objects.select_for_update().get(id=item.product.id)
            product.stock += item.quantity
            product.is_available = True
            product.save()

    order.status = Order.Status.CANCELLED
    order.save(update_fields=['status'])

    OrderStatusHistory.objects.create(
        order=order,
        status='cancelled',
        note='Order was cancelled by the user.',
        created_by=request.user
    )

    send_order_status_email(order)

    messages.success(
        request,
        'Your order has been cancelled. Books returned to stock.'
    )

    return redirect('users:profile')
