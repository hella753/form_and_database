from django import forms
from order.models import CartItems


class CartItemForm(forms.ModelForm):

    class Meta:
        model = CartItems
        fields =  '__all__'
        # exclude = []

