from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect
from store.models import Product, ProductReviews, Category, ShopReviews, ProductTags
from order.models import Cart, CartItems
from store.helpers import counting, add_to_cart


def index(request):
    cart = Cart.objects.get(user=request.user)
    cartitems = CartItems.objects.filter(cart=cart)
    cart_count = cartitems.aggregate(cart_count=Count("id"))

    if type(cart_count) == dict:
        cart_count = cart_count["cart_count"]

    reviews = ShopReviews.objects.all().select_related("user")
    if request.GET.get('q'):
        return redirect(f"/store/category/?q={request.GET.get('q')}")
    context = {
        "reviews": reviews,
        "cart_count": cart_count
    }
    return render(request, "homepage/index.html", context)


def category_listings(request, slug=None):
    # ვიღებთ კატეგორიებს რომლებსაც არ ყავთ მშობლები
    categories = Category.objects.all().filter(parent__isnull=True)
    # პროდუქტების ინიციალიზაცია
    products = Product.objects.prefetch_related("tags")
    # ვიღებთ თეგებს
    product_tags = ProductTags.objects

    # თუ სლაგი არ გადმოეცა ანუ კატეგორიის მიხედვით არ ვფილტრავთ
    if slug is None:
        # მოგვაქვს პროდუქტები კატეგორიებითა და ტეგებით
        products = Product.objects.prefetch_related("product_category", "tags")
        # აგრეგაციისთვის ფუნქცია
        counting(categories, products)
    else:
        # თუ სლაგი გადმოეცა ანუ რომელიმე კატეგორიაში ვართ.
        selected_category = Category.objects.filter(slug=slug)
        categories = selected_category.get_descendants(include_self=True)
        products = Product.objects.filter(
            product_category__in=categories
        ).prefetch_related("tags")
        categories = selected_category.get_descendants(include_self=False)
        # აგრეგაციისთვის ფუნქცია
        counting(categories, products)

    # ძებნისთვის. თუ 'q' ამოიღებს პროდუქტები გავფილტროთ.
    # გაითვალისწინეთ რომ ძიება და ფილტრაცია ერთდროულად არ ხდება.
    # რადგან დიზაინს მირევდა ერთ ფორმაში თუ ვსვამდი ყველაფერს 😭.
    if request.GET.get('q'):
        q = request.GET.get('q')
        products = Product.objects.filter(
            product_name__icontains=q
        ).prefetch_related("tags")

    # სორტირებისთვის მაგრამ პაგინაციასთან ერთად არ მუშაობას.
    # მოგვიანებით მივუბრუნდები.
    if request.POST.get('fruitlist'):
        fruit_list = request.POST.get('fruitlist')
        if fruit_list=="2":
            products = Product.objects.order_by("product_price")

    # ფილტრაციისთვის. თუ 'p' ამოიღებს ფასის მიხედვით. 't' ტეგების მიხედვით.
    if request.GET.get('p') or request.GET.get('t'):
        products = Product.objects.filter(
            product_price__lte=request.GET.get('p'),
            tags=request.GET.get('t')
        ).prefetch_related("tags")

    # გვჭირდება კალათის ამოღება რადგან გამოვაჩინოთ კონკრეტული
    # მომხმარებლის კალათის პროდუქტების რაოდენობა
    cart = Cart.objects.get(user=request.user)
    cartitems = CartItems.objects.filter(
        cart=cart
    ).prefetch_related("product__tags")
    cart_count = cartitems.aggregate(cart_count=Count("id"))

    # პაგინაციისთვის
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    products_objects = paginator.get_page(page_number)

    # თუ POST მეთოდი იქნება დავამატოთ კალათაში პროდუქტი
    # და განვაახლოთ cart_count
    if request.POST.get("name"):
        add_to_cart(request, products, cart)
        cart_count = cartitems.aggregate(cart_count=Count("id"))
    # ტიპს ვამოწმებ და ისე ვანიჭებ თორემ იბნევა პითონი
    if type(cart_count) == dict:
        cart_count = cart_count["cart_count"]

    context = {
        "categories": categories,
        "products": products.prefetch_related("tags"),
        "featured_prod_iterator": range(0, 3),
        'products_objects': products_objects,
        'paginator': paginator,
        'cart_count': cart_count,
        'product_tags': product_tags,
        'get_param': request.GET,
    }
    return render(request, "shop/shop.html", context)


def contact(request):
    return render(request, "contact/contact.html")


def product(request, slug):
    # ვიღებთ პროდუქტს და მის შეფასებებს
    individual_product = Product.objects.get(slug=slug)
    product_reviews = ProductReviews.objects.filter(
        product=individual_product
    ).select_related("user")
    categories = Category.objects.all().filter(parent__isnull=True)
    products = Product.objects.prefetch_related("product_category", "tags")
    counting(categories, products)
    quantity = 1

    # კალათისთვის
    cart = Cart.objects.get(user=request.user)
    cartitems = CartItems.objects.filter(
        cart=cart
    ).prefetch_related("product__tags")
    cart_count = cartitems.aggregate(cart_count=Count("id"))

    if request.GET.get('q'):
        return redirect(f"/store/category/?q={request.GET.get('q')}")

    if request.method == "POST":
        quantity = int(request.POST.get('product_quantity'))
        add_to_cart(
            request,
            individual_product,
            cart,
            quantity,
            from_detail=True
        )
        cart_count = cartitems.aggregate(cart_count=Count("id"))

    if type(cart_count) == dict:
        cart_count = cart_count["cart_count"]

    context = {
        "product": individual_product,
        "categories": categories,
        "product_reviews": product_reviews,
        "quantity": quantity,
        'cart_count': cart_count,
    }

    return render(request, "product_detail/shop-detail.html", context)
