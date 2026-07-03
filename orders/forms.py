from django import forms
from .models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'full_name', 'phone', 'country', 'city',
            'postal_code', 'address_line1', 'address_line2',
            'is_default'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+44...'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '01001'}),
            'address_line1': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Street, house, apartment'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Additional information'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'address_line2' and field_name != 'is_default':
                field.required = True


class OrderCheckoutForm(forms.Form):
    PAYMENT_CHOICES = [
        ('cash', 'Cash on delivery'),
        ('card', 'Online card payment'),
        ('bank', 'Bank transfer'),
    ]

    payment_method = forms.ChoiceField(
        label='Method of payment',
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    notes = forms.CharField(
        label='Comment on the order',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    agree_terms = forms.BooleanField(
        label='I agree to the delivery and payment terms',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
