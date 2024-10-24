from django.db.models import Sum, Count
from django.shortcuts import render
from order.models import Cart
from order.models import CartItems


def cart(request):
    cartitems = CartItems.objects.filter(cart__user__username="admin").select_related("product").all()
    subtotal=0
    total = 0
    cart = Cart.objects.get(user__username="admin")
    cart_count = cartitems.aggregate(cart_count=Count("id"))

    if len(cartitems)!=0:
        subtotal = cartitems.aggregate(total=Sum("total_price")).get("total")
        total = subtotal + cart.flat_rate
    context={
        "cartitems": cartitems,
        "subtotal": subtotal,
        "total": total,
        "cart": cart,
        "cart_count": cart_count["cart_count"]
    }
    return render(request, "cart/cart.html", context)


def checkout(request):
    cartitems = CartItems.objects.filter(cart__user__username="admin").select_related("product").all()
    cart = Cart.objects.get(user__username="admin")
    cart_count = cartitems.aggregate(cart_count=Count("id"))
    subtotal = cartitems.aggregate(total=Sum("total_price")).get("total")
    total = subtotal + cart.flat_rate
    context={
        "cartitems": cartitems,
        "total": total,
        "subtotal": subtotal,
        "cart": cart,
        "cart_count": cart_count["cart_count"]
    }
    return render(request, "checkout/chackout.html", context)