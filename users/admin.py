
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_email_verified', 'is_active', 'is_staff')

    list_editable = ('is_active', 'is_staff')

    list_filter = ('is_active', 'is_email_verified', 'is_staff', 'is_superuser', 'date_joined')

    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = (
        ('Account Credentials', {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Verification & Security', {
            'description': 'Status of user activation and shop verification.',
            'fields': ('is_active', 'is_email_verified')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
