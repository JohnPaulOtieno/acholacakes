from django import forms
from store.models import AddOn

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int
    )
    custom_message = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Pipe a message (e.g. Happy Birthday)'}))
    addons = forms.ModelMultipleChoiceField(
        queryset=AddOn.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
