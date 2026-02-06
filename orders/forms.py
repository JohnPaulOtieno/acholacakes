from django import forms
from .models import Order
from django.utils import timezone
from datetime import timedelta

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city', 'fulfillment_method',
                  'delivery_date', 'special_instructions']
        widgets = {
             'address': forms.TextInput(attrs={'placeholder': 'Street Address'}),
             'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_delivery_date(self):
        date = self.cleaned_data['delivery_date']
        if date:
            if date < timezone.now().date() + timedelta(days=2):
                raise forms.ValidationError("Orders must be placed at least 48 hours in advance.")
        return date
