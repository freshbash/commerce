from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add/", views.add , name="addlisting"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/<int:item_id>/", views.delete_from_watchlist, name="deleteFromWatchlist"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("listing/bid/<int:listing_id>/", views.bid, name="bid"),
    path("listing/close/<int:listing_id>/", views.close, name="close"),
    path("listing/addedcomment/<int:listing_id>/", views.addcomment, name="addcomment"),
    path("categories/", views.categories, name="categories"),
    path("categorylist/<str:category>/", views.catlist, name="catlist"),
    path("profile/<str:username>/", views.profile, name="profile")
]
