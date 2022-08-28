from cProfile import label
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment, Watchlist


def index(request):
    if "watchlist" not in request.session:
        request.session["watchlist"] = []
    listings = list(Listing.objects.all())
    return render(request, "auctions/index.html", {
        "listings": listings, 
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

class CreateListingForm(forms.Form):
    title = forms.CharField(label="Title")
    desc = forms.CharField(label="Description")
    start = forms.DecimalField(decimal_places=2, label="Enter Starting bid")
    url = forms.URLField(label="Enter Image URL")

    CATEGORY_CHOICES = [
        ("ANTIQUES", "Antiques"),
        ("AUTOMOBILES", "Automobiles"),
        ("BOOKS", "Books/Textbooks",), 
        ("ELECTRONICS", "Electronics",), 
        ('FASHION', "Fashion",), 
        ("TOYS", "Toys",), 
        ("HOME", "Home/Kitchen",),
        ]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label="Select Category")

@login_required(redirect_field_name=None, login_url="/login")
def add(request):
    if request.method == "POST":
        name = request.POST["title"]
        desc = request.POST["desc"]
        start = float(request.POST["start"])
        url = request.POST["url"]
        cat = request.POST["cat"].upper()

        listing = Listing(
            user = request.user,
            title=name.capitalize(),
            description=desc,
            starting_bid=start,
            current_price=start,
            image_url=url, category=cat)
        listing.save()

        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/add.html", {
            "form": CreateListingForm
        })

@login_required(redirect_field_name=None, login_url="/login")
def listing(request, listing_id, add=0, bid_valid=None):
    details = Listing.objects.get(pk=listing_id)
    if add:
        watchlist = Watchlist(user=request.user, listing=details)
        watchlist.save()
    flag = False
    if (Watchlist.objects.filter(user=request.user).filter(listing=details)):
        flag = True
    status = False
    if details.status in ["A", "Active"]:
        status = True
    max_bidder = None
    if status == False:
        bids_for_listing = list(Bid.objects.filter(listing=details))
        max_bid = 0
        for bid in bids_for_listing:
            if bid.bid > max_bid:
                max_bid = bid.bid
                max_bidder = bid.user
    
    comments = list(Comment.objects.filter(listing=details))
    return render(request, "auctions/listing.html", {
        "details": details, "flag": flag, "bid_valid":bid_valid, "status": status, "max_bidder": max_bidder,
        "comments": comments
    })

@login_required(redirect_field_name=None, login_url="/login")
def watchlist(request):
    data = list(Watchlist.objects.filter(user=request.user))
    return render(request, "auctions/watchlist.html", {
        "data": data
    })

def delete_from_watchlist(request, item_id):
    if item_id is not None:
        item = Listing.objects.get(pk=item_id)   
        Watchlist.objects.filter(user=request.user).filter(listing=item).delete()
    return HttpResponseRedirect(f"/watchlist/")

@login_required(redirect_field_name=None, login_url="/login")
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
    return HttpResponseRedirect(f"/listing/{listing_id}/{0}/{int(valid)}/")

@login_required(redirect_field_name=None, login_url="/login")
def close(request, listing_id):
    item = Listing.objects.get(pk=listing_id)
    item.status = "D"
    item.save()
    return HttpResponseRedirect(f"/listing/{listing_id}/")

@login_required(redirect_field_name=None, login_url="/login")
def addcomment(request, listing_id):
    detail = request.POST["comment"]
    item = Listing.objects.get(pk=listing_id)
    comment = Comment(user=request.user, listing=item, comment=detail)
    comment.save()
    return HttpResponseRedirect(f"/listing/{listing_id}/")

@login_required(redirect_field_name=None, login_url="/login")
def categories(request):
    cat = [c for c in Listing.category.field.choices]
    return render(request, "auctions/categories.html", {
        "cat": cat
    })

@login_required(redirect_field_name=None, login_url="/login")
def catlist(request, category):
    listings = list(Listing.objects.filter(category=category).filter(status="A"))
    return render(request, "auctions/catlist.html", {
        "listings": listings, "category": category.capitalize()
    })
