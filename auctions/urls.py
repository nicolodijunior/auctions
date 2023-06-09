from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("<int:listing_id>/end_listing", views.end_listing, name="end_listing"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("categories/<str:category_name>", views.category_listings, name="category_listings"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),
    path("<int:listing_id>/remove_from_watchlist", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("<int:listing_id>/make_bid", views.make_bid, name="make_bid"),
    path("<int:listing_id>/make_comment", views.make_comment, name="make_comment"),
]
