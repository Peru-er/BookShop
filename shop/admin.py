
from django.contrib import admin
from .models import (
    Category,
    Product,
    ProductImage,
    Author,
    Series,
    Genre,
    CarouselBanner,
    Discount,
    Review
)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_percent', 'start_date', 'end_date', 'is_active', 'is_currently_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('name',)

    fieldsets = (
        ('General Information', {
            'fields': ('name', 'discount_percent', 'is_active')
        }),
        ('Duration Period', {
            'fields': ('start_date', 'end_date')
        }),
        ('Apply Discount To', {
            'description': 'Select targets for this discount. Leave fields blank if not applicable.',
            'fields': ('categories', 'genres', 'series', 'products')
        }),
    )

    autocomplete_fields = ['categories', 'genres', 'series', 'products']


@admin.register(CarouselBanner)
class CarouselBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'price', 'stock', 'is_available']
    list_filter = ['is_available', 'category']
    list_editable = ['price', 'stock', 'is_available']

    search_fields = ['name', 'isbn', 'author__name']

    fieldsets = (
        ('Basic information', {
            'fields': (
                'name',
                'slug',
                'author',
                'series',
                'category',
                'genres'
            )
        }),
        ('Publication details', {
            'fields': (
                'publisher',
                'publication_year',
                'isbn',
                'pages',
                'language',
                'age_rating',
                'format'
            )
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Store information', {
            'fields': (
                'price',
                'stock',
            )
        }),
    )

    prepopulated_fields = {'slug': ('name',)}

    autocomplete_fields = [
        'author',
        'series',
        'category',
        'genres'
    ]

    inlines = [ProductImageInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'is_verified_purchase', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'created_at')
    search_fields = ('user__username', 'product__name', 'text')
