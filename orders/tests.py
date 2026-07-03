
from django.test import TestCase
from django.contrib.auth import get_user_model
from shop.models import Category, Author, Product
from .models import Order, ShippingAddress
from .views import create_order


User = get_user_model()


class MockRequest:
    def __init__(self, user):
        self.user = user
        self._messages = MockMessageStorage()


class MockMessageStorage:

    def add(self, level, message, extra_tags=''):
        pass


class OrderStockTransactionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='password123')

        self.address = ShippingAddress.objects.create(
            user=self.user,
            full_name="John Doe",
            phone="+4412345678",
            city="London",
            postal_code="E1 6AN",
            address_line1="221B Baker Street"
        )

        self.author = Author.objects.create(name="Arthur Conan Doyle")
        self.category = Category.objects.create(name="Detective", slug="detective")

        # Создаем книгу со stock = 5
        self.product = Product.objects.create(
            category=self.category,
            author=self.author,
            name="Sherlock Holmes",
            slug="sherlock",
            price=12.50,
            stock=5,
            is_available=True
        )

    def test_successful_order_decreases_stock(self):
        fake_cart = [{'product': self.product, 'quantity': 2, 'price': self.product.price}]

        class MockCart(list):
            def get_total_price(self): return 25.00

        cart_instance = MockCart(fake_cart)
        request = MockRequest(self.user)

        order = create_order(
            request=request,
            cart=cart_instance,
            address=self.address,
            payment_method="Card",
            notes="Leave near the door"
        )

        self.assertIsNotNone(order)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)
        self.assertTrue(self.product.is_available)

    def test_stock_reaches_zero_makes_product_unavailable(self):
        fake_cart = [{'product': self.product, 'quantity': 5}]

        class MockCart(list):
            def get_total_price(self): return 62.50

        request = MockRequest(self.user)
        order = create_order(request, MockCart(fake_cart), self.address, "Cash", "")

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 0)
        self.assertFalse(self.product.is_available)

    def test_order_fails_if_not_enough_stock(self):
        fake_cart = [{'product': self.product, 'quantity': 10}]

        class MockCart(list):
            def get_total_price(self): return 125.00

        request = MockRequest(self.user)
        order = create_order(request, MockCart(fake_cart), self.address, "Card", "")

        self.assertIsNone(order)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)

        self.assertEqual(Order.objects.count(), 0)
