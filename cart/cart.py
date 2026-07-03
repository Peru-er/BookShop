from decimal import Decimal
from django.conf import settings
from shop.models import Product
from .models import Cart, CartItem
import uuid

class SessionCart:
    """Session-based кошик для анонімних користувачів"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()


class DatabaseCart:
    """Database-based кошик для зареєстрованих користувачів"""

    def __init__(self, request):
        self.request = request
        self.user = request.user

        self.cart, created = Cart.objects.get_or_create(
            user=self.user,
            defaults={
                'cart_code': uuid.uuid4().hex
            }
        )

    def add(self, product, quantity=1, update_quantity=False):
        cart_item, created = CartItem.objects.get_or_create(
            cart=self.cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            if update_quantity:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()

    def remove(self, product):
        CartItem.objects.filter(cart=self.cart, product=product).delete()

    def __iter__(self):
        for item in self.cart.items.select_related('product'):
            yield {
                'product': item.product,
                'quantity': item.quantity,
                'price': item.product.price,
                'total_price': item.product.price * item.quantity  # Спрощений підрахунок
            }

    def __len__(self):
        return sum(item.quantity for item in self.cart.items.all())

    def get_total_price(self):
        return sum(item.product.price * item.quantity for item in self.cart.items.all())

    def clear(self):
        self.cart.items.all().delete()


def get_cart(request):
    if request.user.is_authenticated:
        return DatabaseCart(request)
    else:
        return SessionCart(request)


def merge_carts(request):
    if not request.user.is_authenticated:
        return

    session_cart = SessionCart(request)

    if len(session_cart) == 0:
        return

    db_cart = DatabaseCart(request)

    for item in session_cart:
        db_cart.add(
            product=item['product'],
            quantity=item['quantity']
        )

    session_cart.clear()
