
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from shop.models import Product
from .cart import get_cart


def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def cart_clear(request):
    cart = get_cart(request)
    cart.clear()
    return redirect('cart:cart_detail')


def get_cart_data(cart):
    items = []
    for item in cart:
        product = item['product']
        image_url = ""
        try:
            if product.images.exists() and product.images.first().image:
                image_url = product.images.first().image.url
        except Exception:
            image_url = ""

        author_name = ""
        if getattr(product, 'author', None):
            author_name = getattr(product.author, 'name', str(product.author))

        try:
            price = float(item['price'])
        except Exception:
            price = float(product.current_price)

        try:
            total_price = float(item['total_price'])
        except Exception:
            total_price = price * int(item['quantity'])

        items.append({
            'id': product.id,
            'name': product.name,
            'author': author_name,
            'price': price,
            'quantity': int(item['quantity']),
            'total_price': total_price,
            'image_url': image_url
        })

    try:
        global_total = float(cart.get_total_price())
    except Exception:
        global_total = sum(float(i['price']) * int(i['quantity']) for i in items)

    return {
        'items': items,
        'total_price': global_total,
        'cart_length': int(len(cart))
    }


@require_POST
def cart_add(request, product_id):
    cart = get_cart(request)

    product = get_object_or_404(
        Product.objects.prefetch_related('discounts', 'category__discounts'),
        id=product_id
    )
    quantity = int(request.POST.get('quantity', 1))

    cart.add(product=product, quantity=quantity)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(get_cart_data(cart))

    messages.success(request, f'Item "{product.name}" added to cart')
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
        return JsonResponse(get_cart_data(cart))

    messages.success(request, f'Item "{product.name}" removed from cart')
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    import json
    if request.content_type == 'application/json':
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
    else:
        quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        cart.add(product=product, quantity=quantity, update_quantity=True)
        if request.headers.get('x-requested-with') != 'XMLHttpRequest':
            messages.success(request, 'Cart has been updated')
    else:
        cart.remove(product)
        if request.headers.get('x-requested-with') != 'XMLHttpRequest':
            messages.success(request, 'Item removed from cart')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
        return JsonResponse(get_cart_data(cart))

    next_url = request.POST.get('next')
    if next_url and len(cart) > 0:
        return redirect(next_url)

    return redirect('cart:cart_detail')


def cart_data_api(request):
    cart = get_cart(request)
    return JsonResponse(get_cart_data(cart))
