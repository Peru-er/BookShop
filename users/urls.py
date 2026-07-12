
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.profile_settings, name='settings'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/clear/', views.clear_wishlist, name='clear_wishlist'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path(
        'password-reset/',
        views.SuccessMessagePasswordResetView.as_view(
            template_name='users/password_reset/password_reset_form.html',
            email_template_name='emails/password_reset.html',
            success_url='/users/password-reset/done/'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'password-reset-confirm/<uidb64>/<token>/',
        views.CustomPasswordResetConfirmView.as_view(
            template_name='users/password_reset/password_reset_confirm.html',
            success_url='/users/password-reset-complete/'
        ),
        name='password_reset_confirm'
    ),

    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
