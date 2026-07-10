
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Safely creates a superuser if it does not exist yet'

    def handle(self, *args, **options):
        User = get_user_model()

        # Get data from server environment variables
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not password:
            self.stdout.write(self.style.WARNING('DJANGO_SUPERUSER_PASSWORD variable is not set. Skipping.'))
            return

        if not User.objects.filter(username=username).exists():
            admin_user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" successfully created!'))
        else:
            self.stdout.write(self.style.INFO(f'User "{username}" already exists.'))
