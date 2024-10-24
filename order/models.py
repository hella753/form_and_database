from django.db import models
from django.contrib.auth.models import User


class Checkout(models.Model):
    first_name = models.CharField("სახელი", max_length=100)
    last_name = models.CharField("გვარი", max_length=100)
    order_address = models.CharField(max_length=100, verbose_name="მისამართი")
    city = models.CharField("ქალაქი", max_length=100)
    country = models.CharField("ქვეყანა", max_length=100)
    postcode = models.IntegerField("საფოსტო კოდი")
    mobile = models.CharField("ტელეფონის ნომერი", max_length=100)
    email = models.EmailField("მეილი", max_length=100)

    create_account = models.BooleanField("შექმენი ანგარიში", default=False)
    order_notes = models.TextField("შეკვეთის დეტალები")

    order_date = models.DateField("შეკვეთის თარიღი", auto_now_add=True)
    product_cart = models.ForeignKey(
        "order.Cart",
        on_delete=models.CASCADE,
        verbose_name="პროდუქტები",
    )
    order_customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="მომხმარებელი"
    )

    def __str__(self):
        return f"Order {self.id} | status {self.order_status}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name="მომხმარებელი")
    flat_rate = models.IntegerField("მიტანა")

    def __str__(self):
        return f"{self.user}"


class CartItems(models.Model):
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE, verbose_name="პროდუქტი")
    product_quantity = models.IntegerField("რაოდენობა")
    cart = models.ForeignKey("order.Cart", on_delete=models.CASCADE, verbose_name="კალათა")
    total_price = models.IntegerField("მთლიანი ფასი", null=True, blank=True)

    def get_total_price(self):
        return self.product.product_price * self.product_quantity

    def save(self, *args, **kwargs):
        self.total_price = self.get_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} | {self.product_quantity} | {self.cart}"