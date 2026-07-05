
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from orders.models import Order
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django_ratelimit.decorators import ratelimit

from cart.cart import merge_carts


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

    return render(request, 'users/profile.html', {
        'active_orders': active_orders,
    })
