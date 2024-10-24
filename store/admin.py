from django.contrib import admin
from store.models import Category, Product, ProductReviews, ShopReviews, ProductTags

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductReviews)
admin.site.register(ShopReviews)
admin.site.register(ProductTags)