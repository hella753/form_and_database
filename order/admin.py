from django.contrib import admin
from order.models import Checkout, Cart, CartItems

# Register your models here.
admin.site.register(Checkout)
admin.site.register(Cart)
admin.site.register(CartItems)