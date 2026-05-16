from django.urls import path

from . import views


urlpatterns = [

    # HOME
    path('', views.home, name='home'),

    # BOOK DETAILS
    path(
        'book/<int:id>/',
        views.book_detail,
        name='book_detail'
    ),

    # SEARCH
    path(
        'search/',
        views.search_books,
        name='search'
    ),

    # CART
    path(
        'add-to-cart/<int:book_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'remove-from-cart/<int:cart_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    # WISHLIST
    path(
        'wishlist/<int:book_id>/',
        views.add_to_wishlist,
        name='add_to_wishlist'
    ),

    path(
        'wishlist/',
        views.wishlist,
        name='wishlist'
    ),

    path(
        'wishlist/remove/<int:item_id>/',
        views.remove_wishlist,
        name='remove_wishlist'
    ),

    # AUTHENTICATION
    path('register/', views.register_view, name='register'),
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
    # CHECKOUT
    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
    'generate-summary/<int:book_id>/',
    views.generate_summary,
    name='generate_summary'
),
path('category/<int:id>/', views.category_books, name='category_books'),

path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

path('subscribe/', views.subscribe, name='subscribe'),


]