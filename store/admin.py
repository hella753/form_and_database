from django.contrib import admin
from store.models import Category, Product, ProductReviews, ShopReviews, ProductTags

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("category_name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("product_name",)}


admin.site.register(ProductReviews)
admin.site.register(ShopReviews)
admin.site.register(ProductTags)