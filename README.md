# Create Or Optimized Models for Design & Submit GET-POST Forms


## Description 
Fruit and Vegetable shop website made with free template.
The Project uses Django and sqlite3 database. 
There are several records in the database for testing.

## **Features** ##
* with the help of `forms.py` new product is added in the cart.
* Products, Categories, ProductTags, orders, reviews can be added from the admin panel.
* `CartItem` object is created every time the user presses the **"Add to Cart"** button either from the **shop** page or **product detail** page. User's cart is assigned to CartItem. Before the item gets added program checks if there is products of this amount left in the database.
* Pagination works with filtering and search as well. (Not with sorting tho. I'll get back to it later)
* Search bar is working on homepage in both searching places: In **modal** and in **header**. It works on the Shop and Product Detail pages. **Filters the products by name.** Redirects to store:shop if the current url is different.
* store/category has 2 root categories. They are both displayed in dropdown menu in navbar and have their urls but use the same view as shop.
* Cart items count is displayed on the navbar cart icon. Cart items are also displayed on the order:cart and order:checkout
* Slug is automatically generated with the help of Custom Admin.


## **Components** ##
* **store** - This app contains the 5 models(Product, Category, ProductReviews, ShopReviews and ProductTags). Models are self-explanatory. Has 4 views for homepage, contact, product detail and shop.
  * **store/helpers.py** - `counting()` and `add_to_cart()` functions are in here for better organization of views.
* **order** - This app contains the models(Checkout(which is the order basically), Cart and CartItems) and 2 views for the cart and checkout.
* **media** - All user uploaded images go to the media folder.
* **static** - for static files: JS, CSS, Images that is being used are all stored there.
* **templates** - avaialable templates.
* **db.sqlite3** - Database file.


### Templates
  * cart - in this directory there are components for cart, base_cart.html and cart.html.
  * checkout - in this directory there are components for checkout and base_checkout.html and checkout.html.
  * contact - in this directory there are components for contact and base_contact.html and contact.html.
  * homepage - in this directory there are components for homepage and base_index.html and index.html.
  * product_detail - in this directory there are components for product_detail and base_detail.html and shop-detail.html.
  * shop - in this directory there are components for shop and base_shop.html and shop.html.
  * reusable_components - Here are some reusable components that I'm using through templates and apps such as navbar, spinner and search.
  * base.html - The main base html file where all the shared code is which then is inherited in other templates.
  * footer.html - Footer component

### URLS
  * Home - is accessible on route `store/`
  * Shop - is accessible on route `store/category/` or `store/category/xili/` or `store/category/bostneuli/`. you can access it from the dropdown menu in navbar as well.
  * Detail - is accessible on route `store/product/jolo/`. Change the raspberry with product name if needed. You can access the detail page from the shop when you click on the product as well. 
  * Contact - is accessible on route `contact/`
  * Cart - is accessible on route `order/cart/`. You can also access this page by clicking the cart icon in the navbar 
  * Checkout - is accessible on route `order/checkout/`.
  * Admin Panel - is accessible on `admin/`. Username is 'admin' and password is 'admin'.


## Dependencies
* **Python 3.X**
* **Django 5.1.1**
* **Pillow 11.0.0** - Python Imaging Library adds image processing capabilities to your Python interpreter.
* **Django-debug-toolbar** - Configurable set of panels that display various debug information about the current request/response.
* **Django-mptt** - Reusable Django app which aims to make it easy for you to use MPTT(a technique for storing hierarchical data in a database).
* **django-versatileimagefield~=3.1**


## Usage
Clone the repository:
```bash
git clone https://github.com/hella753/form_and_database.git
cd form_and_database
```
To install the dependencies, use the following command in your terminal:
```bash
pip install -r requirements.txt
```
To run the development server, use the following command in your terminal:
```bash
python manage.py runserver
```
To access the application, open your browser and go to http://127.0.0.1:8000/
