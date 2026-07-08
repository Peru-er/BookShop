from django.db.models import Q, Case, Value, When, IntegerField
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect

from users.models import Wishlist
from .models import (
    Product,
    Category,
    Genre,
    Author,
    Series,
    Waitlist
)


def home(request):
    products = Product.objects.select_related('author').prefetch_related('images').all()[:8]

    wished_products_ids = []
    if request.user.is_authenticated:
        wished_products_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    return render(request, 'shop/home.html', {
        'products': products,
        'wished_products_ids': wished_products_ids
    })


def catalog(request):
    products = Product.objects.select_related('author', 'series').prefetch_related('images').annotate(
        out_of_stock=Case(
            When(stock=0, then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by('out_of_stock', 'name')

    wished_products_ids = []
    if request.user.is_authenticated:
        wished_products_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    categories = cache.get('shop_categories')
    if not categories:
        categories = Category.objects.all()
        cache.set('shop_categories', categories, 86400)

    genres = cache.get('shop_genres')
    if not genres:
        genres = Genre.objects.all()
        cache.set('shop_genres', genres, 86400)

    authors = cache.get('shop_authors')
    if not authors:
        authors = Author.objects.all().order_by('name')
        cache.set('shop_authors', authors, 86400)

    series_list = cache.get('shop_series')
    if not series_list:
        series_list = Series.objects.all().order_by('name')
        cache.set('shop_series', series_list, 86400)

    query = request.GET.get('q')

    author = request.GET.get('author')
    series = request.GET.get('series')
    publisher = request.GET.get('publisher')
    category = request.GET.get('category')
    selected_genres = request.GET.getlist('genre')
    language = request.GET.get('language')
    book_format = request.GET.get('format')
    age_rating = request.GET.get('age_rating')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(author__name__icontains=query)
        ).distinct()

    if author:
        products = products.filter(author_id=author)

    if series:
        products = products.filter(series_id=series)

    if publisher:
        products = products.filter(publisher=publisher)

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

    if min_price:
        products = products.filter(price__gte=max(0, float(min_price)))

    if max_price:
        products = products.filter(price__lte=max(0, float(max_price)))

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

    publishers = (
        Product.objects
        .exclude(publisher__isnull=True)
        .exclude(publisher__exact='')
        .values_list('publisher', flat=True)
        .distinct()
        .order_by('publisher')
    )

    return render(request, 'shop/catalog.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'genres': genres,
        'authors': authors,
        'series_list': series_list,
        'publishers': publishers,

        'languages': languages,
        'formats': formats,
        'age_ratings': age_ratings,

        'selected_author': author,
        'selected_series': series,
        'selected_publisher': publisher,
        'selected_category': category,
        'selected_genres': selected_genres,
        'selected_language': language,
        'selected_format': book_format,
        'selected_age_rating': age_rating,
        'min_price': min_price,
        'max_price': max_price,

        'wished_products_ids': wished_products_ids,
    })


def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.select_related('author', 'series').prefetch_related('genres'),
        pk=pk
    )

    recently_viewed = request.session.get('recently_viewed', [])

    if product.id in recently_viewed:
        recently_viewed.remove(product.id)

    recently_viewed.insert(0, product.id)

    request.session['recently_viewed'] = recently_viewed[:10]

    request.session.modified = True

    is_wished = False
    if request.user.is_authenticated:
        is_wished = Wishlist.objects.filter(user=request.user, product=product).exists()

    context = {
        'product': product,
        'is_wished': is_wished,
    }
    return render(request, 'shop/product_detail.html', context)


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    products = author.products.all()

    from_product_id = request.GET.get('from_product')
    from_product = None
    if from_product_id:
        try:
            from_product = Product.objects.get(id=from_product_id)
        except Product.DoesNotExist:
            pass

    context = {
        'author': author,
        'products': products,
        'from_product': from_product,
    }
    return render(request, 'shop/author_detail.html', context)


def subscribe_to_stock(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            email = request.user.email
            user = request.user
        else:
            email = request.POST.get('email')
            user = None

        if not email:
            messages.error(request, "Please provide a valid email address.")
            return redirect('shop:product_detail', pk=product_id)

        exists = Waitlist.objects.filter(email=email, product=product, is_notified=False).exists()

        if exists:
            messages.info(request, "You are already on the waitlist for this book.")
        else:
            Waitlist.objects.create(user=user, email=email, product=product)
            messages.success(request, "We will notify you as soon as this book is back in stock.")

    return redirect('shop:product_detail', pk=product_id)
