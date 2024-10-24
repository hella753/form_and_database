from django.db.models import Count
from order.forms import CartItemForm
from order.models import CartItems


def counting(categories, products):
    for category in categories:
        # ვიღებთ შვილ კატეგორიებს და ვფილტრავთ პროდუქტებს იმის მიხედვით არიან თუ არა ამ კატეგორიებში.
        subcategories = category.get_descendants(include_self=True)
        products_in_category = products.filter(
            product_category__in=subcategories
        )
        # ვაკეთებთ აგრეგაციას რომ გამოჩნდეს თითოეულ კატეგორიაში რამდენი პროდუქტია
        count = products_in_category.aggregate(
            products_count=Count("id")
        )
        category.product_count = count["products_count"]

def add_to_cart(request, products, cart, quantity=1, from_detail=False):
    # ვიღებ პროდუქტის ნეიმს და ვფილტრავ ამის მიხედვით
    name = request.POST.get("name")

    if from_detail:
        # თუ პროდუქტის დეტალური გვერდიდან არის მოსული დამატების მოთხოვნა
        individual_product = products
    else:
        individual_product = products.filter(product_name=name).first()

     # თუ არ არის პროდუქტი მარაგში არ ემატება
    if quantity > individual_product.product_quantity:
        print("მარაგში არ გვაქვს ეს პროდუქტი ამ რაოდენობით")
    else:
        total_price = individual_product.product_price * quantity
        # ვქმნით კალათის აითემების ობიექტს.
        cart_item = CartItems(product=individual_product, product_quantity=quantity, cart=cart, total_price=total_price)
        # ვქმნით ფორმას და ვაწვდით ახლად შექმნილ ობიექტს
        form = CartItemForm(instance=cart_item)
        new_item = form.save(commit=False)
        # ვასეივებთ ახალ აითემს
        new_item.save()


