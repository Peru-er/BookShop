
from django.db import models
from ecommerce_project import settings


class Series(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Name', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField('Description', blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Parent category'
    )
    is_active = models.BooleanField('Active', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    genres = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='books'
    )
    COVER_CHOICES = [
        ('Paperback', 'Paperback'),
        ('Hardcover', 'Hardcover'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='products'
    )

    publisher = models.CharField(max_length=150, blank=True)
    publication_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    series = models.ForeignKey(
        Series,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )
    isbn = models.CharField(max_length=20, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=50, default='English')
    age_rating = models.CharField(max_length=10, blank=True)

    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    format = models.CharField(
        max_length=20,
        choices=COVER_CHOICES,
        default='Paperback'
    )
    stock = models.PositiveIntegerField(default=10)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Image for {self.product.name}'


class Waitlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='waitlist_subscribers')
    created_at = models.DateTimeField(auto_now_add=True)
    is_notified = models.BooleanField(default=False)

    class Meta:
        unique_together = ('email', 'product')

    def __str__(self):
        return f"{self.email} waiting for {self.product.name}"


class CarouselBanner(models.Model):
    title = models.CharField(max_length=200, verbose_name="Banner Title")
    description = models.TextField(blank=True, verbose_name="Description / Promotion")
    image = models.ImageField(upload_to='carousel_banners/', verbose_name="Banner Image")
    link = models.CharField(max_length=200, blank=True, help_text="URL path where the user redirects (e.g., /catalog/?category=1)")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Carousel Banner"
        verbose_name_plural = "Carousel Banners"

    def __str__(self):
        return self.title
