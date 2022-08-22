from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment


def index(request):
    if "watchlist" not in request.session:
        request.session["watchlist"] = []
    listings = list(Listing.objects.all())
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first = request.POST["first_name"]
        last = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=first, last_name=last)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(redirect_field_name=None, login_url="/login")
def add(request):
    if request.method == "POST":
        name = request.POST["title"]
        desc = request.POST["desc"]
        start = float(request.POST["start"])
        url = request.POST["url"]
        cat = request.POST["cat"]

        listing = Listing(
            user = request.user,
            title=name,
            description=desc,
            starting_bid=start,
            current_price=start,
            image_url=url, category=cat)
        listing.save()

        return index(request)

    else:
        return render(request, "auctions/add.html")

@login_required(redirect_field_name=None, login_url="/login")
def listing(request, listing_id, add=None, bid_valid=None):
    details = Listing.objects.get(pk=listing_id)
    if add:
        item = dict()
        item["id"] = details.id
        item["title"] = details.title
        item["url"] = details.image_url
        item["price"] = details.current_price
        request.session["watchlist"] += [item]
    flag = False
    for item in request.session["watchlist"]:
        if item["id"] ==  details.id:
            flag = True
            break
    status = False
    if details.status in ["A", "Active"]:
        status = True
    if status == False:
        bids_for_listing = list(Bid.objects.filter(listing=details))
        max_bidder = None
        max_bid = 0
        for bid in bids_for_listing:
            if bid.bid > max_bid:
                max_bid = bid.bid
                max_bidder = bid.user
    return render(request, "auctions/listing.html", {
        "details": details, "flag": flag, "bid_valid":bid_valid, "status": status, "max_bidder": max_bidder
    })

@login_required(redirect_field_name=None, login_url="/login")
def watchlist(request, item_id=None):
    if item_id is not None:   
        request.session['watchlist'] = [
            item for item in request.session['watchlist'] if item['id'] != item_id
            ]
    data = request.session["watchlist"]
    return render(request, "auctions/watchlist.html", {
        "data": data
    })    

def bid(request, listing_id):
    bid = float(request.POST["bid"])
    details = Listing.objects.get(pk=listing_id)
    valid = False
    if bid >= details.starting_bid and bid > details.current_price:
        valid = True
        details.current_price = bid
        details.save()
        new_high_bidder = Bid(user=request.user, listing=details, bid=bid)
        new_high_bidder.save()
    return listing(request, listing_id=listing_id, bid_valid=valid)

def close(request, listing_id):
    pass
