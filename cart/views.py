from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import get_cart


def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def cart_clear(request):
    cart = get_cart(request)
    cart.clear()
    return redirect('cart:cart_detail')


@require_POST
def cart_add(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get('quantity', 1))

    cart.add(product=product, quantity=quantity)
    messages.success(request, f'Item "{product.name}" added to cart')

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    messages.success(request, f'Item "{product.name}" removed from cart')
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        cart.add(product=product, quantity=quantity, update_quantity=True)
        messages.success(request, 'Cart has been updated')
    else:
        cart.remove(product)
        messages.success(request, 'Item removed from cart')

    return redirect('cart:cart_detail')
