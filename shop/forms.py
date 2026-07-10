
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(
                choices=[('', 'Select rating')] + [(i, f"{i} ★") for i in range(5, 0, -1)],
                attrs={'class': 'form-select mb-3'}
            ),
            'text': forms.Textarea(
                attrs={'class': 'form-control mb-3', 'rows': 4, 'placeholder': 'Write your review here...'}
            ),
        }
