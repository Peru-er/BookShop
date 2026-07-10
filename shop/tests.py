
from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Author, Product

class ShopModelsTestCase(TestCase):
    def setUp(self):

        self.author = Author.objects.create(name="J.K. Rowling")
        self.category = Category.objects.create(name="Fantasy", slug="fantasy")
        self.product = Product.objects.create(
            category=self.category,
            author=self.author,
            name="Harry Potter",
            slug="harry-potter",
            price=15.99,
            stock=5,
            is_available=True
        )

    def test_category_creation(self):

        self.assertEqual(self.category.name, "Fantasy")
        self.assertEqual(str(self.category), "Fantasy")

    def test_product_creation(self):

        self.assertEqual(self.product.name, "Harry Potter")
        self.assertEqual(str(self.product), "Harry Potter")
        self.assertEqual(self.product.stock, 5)


class ShopViewsTestCase(TestCase):
    def setUp(self):

        self.client = Client()
        self.author = Author.objects.create(name="Test Author")
        self.category = Category.objects.create(name="Test Category", slug="test-cat")
        self.product = Product.objects.create(
            category=self.category,
            author=self.author,
            name="Test Book",
            slug="test-book",
            price=10.00,
            stock=10
        )

    def test_catalog_view_status_code(self):

        response = self.client.get(reverse('shop:catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/catalog.html')

    def test_product_detail_view(self):

        response = self.client.get(reverse('shop:product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")
