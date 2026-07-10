
from django.test import TestCase
from django.contrib.auth import get_user_model
from shop.models import Category, Author, Product
from .models import Cart, CartItem

User = get_user_model()


class CartModelsTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='password123')

        self.author = Author.objects.create(name="Test Author")
        self.category = Category.objects.create(name="Test Category", slug="test-cat")
        self.product = Product.objects.create(
            category=self.category,
            author=self.author,
            name="Django Book",
            slug="django-book",
            price=20.00,
            stock=10
        )

        self.cart = Cart.objects.create(
            cart_code="test-cart-code-123",
            user=self.user
        )

    def test_cart_creation(self):

        self.assertEqual(self.cart.cart_code, "test-cart-code-123")
        self.assertEqual(self.cart.user, self.user)
        self.assertFalse(self.cart.paid_status)

    def test_cart_item_addition(self):

        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )

        self.assertEqual(cart_item.cart, self.cart)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)

        self.assertEqual(self.cart.items.count(), 1)
        self.assertEqual(self.cart.items.first().product, self.product)
