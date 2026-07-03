
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_order_confirmation_email(order):
    subject = f'Order confirmation #{order.order_number}'

    html_message = render_to_string(
        'orders/emails/order_confirmation.html',
        {'order': order}
    )

    plain_message = (
        f'Thank you for your order!\n\n'
        f'Order number: #{order.order_number}\n'
        f'Total amount: £{order.total_amount}\n\n'
        'Your order is now being processed.'
    )

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.user.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_order_status_email(order):
    subject = f'Order #{order.order_number} status updated'

    html_message = render_to_string(
        'orders/emails/order_status.html',
        {
            'order': order,
        }
    )

    plain_message = f'''
    Your order #{order.order_number}

    New status:
    {order.get_status_display()}
    '''

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.user.email],
        html_message=html_message,
        fail_silently=False,
    )
