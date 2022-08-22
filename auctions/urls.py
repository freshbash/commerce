from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add/", views.add , name="addlisting"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("listing/<int:listing_id>/<add>/", views.listing, name="listingadd"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/<int:item_id>/", views.watchlist, name="watchlist_del"),
    path("listing/bid/<int:listing_id>/", views.bid, name="bid"),
    path("listing/close/<int:listing_id>/", views.close, name="close")
]
