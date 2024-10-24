from django.urls import path
from . import views

app_name="store"
urlpatterns = [
    path("", views.index, name="index"),
    path("category/", views.category_listings, name="category_listings"),
    path("category/<slug:slug>/", views.category_listings, name="category_listings"),
    path("product/<slug:slug>/", views.product, name="product"),
    path("contact/", views.contact, name="contact")
]
