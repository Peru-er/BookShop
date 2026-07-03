
from django.db.models import Q
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from .models import (
    Product,
    Category,
    Genre,
)


def home(request):

    products = Product.objects.select_related('author').prefetch_related('images').all()[:8]

    return render(
        request,
        'shop/home.html',
        {
            'products': products,
        }
    )


def catalog(request):

    products = Product.objects.select_related('author').prefetch_related('images').all()

    categories = cache.get('shop_categories')
    if not categories:
        categories = Category.objects.all()
        cache.set('shop_categories', categories, 86400)

    genres = cache.get('shop_genres')
    if not genres:
        genres = Genre.objects.all()
        cache.set('shop_genres', genres, 86400)

    query = request.GET.get('q', '')
    category = request.GET.get('category')
    selected_genres = request.GET.getlist('genre')
    language = request.GET.get('language')
    book_format = request.GET.get('format')
    age_rating = request.GET.get('age_rating')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(author__name__icontains=query)
        )

    if category:
        products = products.filter(category_id=category)

    if selected_genres:
        products = products.filter(genres__id__in=selected_genres).distinct()

    if language:
        products = products.filter(language=language)

    if book_format:
        products = products.filter(format=book_format)

    if age_rating:
        products = products.filter(age_rating=age_rating)

    languages = (
        Product.objects
        .exclude(language__isnull=True)
        .exclude(language__exact='')
        .values_list('language', flat=True)
        .distinct()
        .order_by('language')
    )

    formats = (
        Product.objects
        .exclude(format__isnull=True)
        .exclude(format__exact='')
        .values_list('format', flat=True)
        .distinct()
        .order_by('format')
    )

    age_ratings = (
        Product.objects
        .exclude(age_rating__isnull=True)
        .exclude(age_rating__exact='')
        .values_list('age_rating', flat=True)
        .distinct()
        .order_by('age_rating')
    )

    return render(request, 'shop/catalog.html', {
        'products': products,
        'categories': categories,
        'genres': genres,

        'languages': languages,
        'formats': formats,
        'age_ratings': age_ratings,

        'query': query,
        'selected_category': category,
        'selected_genres': selected_genres,
        'selected_language': language,
        'selected_format': book_format,
        'selected_age_rating': age_rating,
    })

def product_detail(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk
    )

    return render(
        request,
        'shop/product_detail.html',
        {
            'product': product,
        }
    )
