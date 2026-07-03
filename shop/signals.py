
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Category, Genre

@receiver([post_save, post_delete], sender=Category)
def invalidate_category_cache(sender, instance, **kwargs):
    cache.delete('shop_categories')

@receiver([post_save, post_delete], sender=Genre)
def invalidate_genre_cache(sender, instance, **kwargs):
    cache.delete('shop_genres')
