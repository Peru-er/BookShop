
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.views import LoginView, LogoutView
from django_ratelimit.decorators import ratelimit
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.http import require_POST

from users.models import Wishlist
from cart.cart import merge_carts
from orders.models import Order
from .forms import RegisterForm, UserProfileForm
from .models import Product


class CustomLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.info(
            request,
            'You have successfully logged out.'
        )
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Welcome back, {form.get_user().username}.'
        )

        response = super().form_valid(form)

        merge_carts(self.request)

        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Incorrect username or password.'
        )
        return super().form_invalid(form)


@ratelimit(key='ip', rate='3/m', block=True)
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                f'Your account has been created successfully. Welcome to BubuKappa, {user.username})'
            )

            return redirect('shop:catalog')

    else:
        form = RegisterForm()

    return render(
        request,
        'users/register.html',
        {
            'form': form
        }
    )


@login_required
def profile(request):

    active_orders = Order.objects.filter(
        user=request.user
    ).prefetch_related('items__product').exclude(
        status__in=['delivered', 'cancelled']
    ).order_by('-created_at')

    order_history = Order.objects.filter(
        user=request.user,
        status__in=['delivered', 'cancelled']
    ).prefetch_related('items__product').order_by('-created_at')

    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')

    return render(request, 'users/profile.html', {
        'active_orders': active_orders,
        'order_history': order_history,
        'wishlist_items': wishlist_items,
    })


@login_required
def profile_settings(request):
    profile_form = UserProfileForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':

        if 'update_profile' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your personal information has been updated successfully.')
                return redirect('users:settings')

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('users:settings')

        # Логика удаления аккаунта
        elif 'delete_account' in request.POST:
            password_to_check = request.POST.get('delete_password')

            if request.user.check_password(password_to_check):
                user = request.user
                auth_logout(request)
                user.delete()
                messages.success(request, 'Your account has been deleted successfully.')
                return redirect('shop:home')
            else:
                messages.error(request, 'Incorrect password. Account was not deleted.')
                return redirect('users:settings')

    return render(request, 'users/settings.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })


@login_required
def toggle_wishlist(request, product_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product = get_object_or_404(Product, id=product_id)
        wish_item = Wishlist.objects.filter(user=request.user, product=product)

        if wish_item.exists():
            wish_item.delete()
            wished = False
            message = f'"{product.name}" removed from wishlist.'
        else:
            Wishlist.objects.create(user=request.user, product=product)
            wished = True
            message = f'"{product.name}" added to wishlist.'

        return JsonResponse({
            'status': 'ok',
            'wished': wished,
            'message': message
        })

    return redirect(request.META.get('HTTP_REFERER', 'users:profile'))


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'users/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
@require_POST
def clear_wishlist(request):
    Wishlist.objects.filter(user=request.user).delete()
    messages.success(request, "Your wishlist has been cleared successfully.")
    return redirect('users:profile')
