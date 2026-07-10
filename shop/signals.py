
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Category, Genre, Product, Waitlist
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@receiver([post_save, post_delete], sender=Category)
def invalidate_category_cache(sender, instance, **kwargs):
    cache.delete('shop_categories')


@receiver([post_save, post_delete], sender=Genre)
def invalidate_genre_cache(sender, instance, **kwargs):
    cache.delete('shop_genres')


@receiver(post_save, sender=Product)
def notify_subscribers_on_stock_arrival(sender, instance, created, **kwargs):
    if not created and instance.stock > 0:
        waiting_list = Waitlist.objects.filter(product=instance, is_notified=False)

        if waiting_list.exists():
            emails = list(waiting_list.values_list('email', flat=True))

            subject = f"'{instance.name}' is back in stock."

            html_message = render_to_string('emails/stock_notification.html', {'product': instance})

            plain_message = strip_tags(html_message)

            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails,
                html_message=html_message,
                fail_silently=True,
            )

            waiting_list.delete()
