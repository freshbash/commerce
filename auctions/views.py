# from cProfile import label
#Import necessary dependencies
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Comment, Watchlist


#Home page of the website. Displays all the listings. Most recent at the top
def index(request):
    if "watchlist" not in request.session:
        request.session["watchlist"] = []
    listings = list(Listing.objects.all())
    listings.reverse()
    return render(request, "auctions/index.html", {
        "listings": listings, 
    })


#Log the user in
def login_view(request):

    #Handle login
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


#Log the user out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


#Register a new  user
def register(request):

    #Handle new registration
    if request.method == "POST":

        #Get the new user's details from the submitted form
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


#Add a listing
@login_required(redirect_field_name=None, login_url="/login")
def add(request):

    #Handle form submission
    if request.method == "POST":

        #Get the data received from the form
        name = request.POST["title"]
        desc = request.POST["desc"]
        start = float(request.POST["start"])
        url = request.POST["url"]
        cat = request.POST["cat"].upper()

        #Create a listing instance
        listing = Listing(
            user = request.user,
            title=name.capitalize(),
            description=desc,
            starting_bid=start,
            current_price=start,
            image_url=url, category=cat
        )

        #Store that instance to the DB
        listing.save()

        #Redirect to the home page.
        return HttpResponseRedirect(reverse("index"))

    else:

        #Display the form to let the user add a listing
        return render(request, "auctions/add.html")

#To be checked. Optimizations possible.
@login_required(redirect_field_name=None, login_url="/login")
def listing(request, listing_id):
    #Get the details of the listing from the db.
    details = Listing.objects.get(pk=listing_id)

    #Checks if the item is added to the watchlist by the user.
    flag = False
    if (Watchlist.objects.filter(user=request.user).filter(listing=details)):
        flag = True

    #Get the comments on the listing
    comments = list(Comment.objects.filter(listing=details))


    return render(request, "auctions/listing.html", {
        "details": details, "flag": flag, "comments": comments
    })

#Add an item to the watchlist or view the watchlist
@login_required(redirect_field_name=None, login_url="/login")
def watchlist(request):
    #If the user adds an item to the watchlist
    if (request.method == "POST"):
        listing_id = request.POST["listing-id"]
        listing_details = Listing(id=listing_id)
        addItemToWatchlist = Watchlist(user=request.user, listing=listing_details)
        addItemToWatchlist.save()
        return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))

    #If the user wants to view the watchlist
    data = list(Watchlist.objects.filter(user=request.user))
    data.reverse()
    return render(request, "auctions/watchlist.html", {
        "data": data
    })


#Delete an item from the watchlist
def delete_from_watchlist(request, item_id):
    if item_id is not None:
        item = Listing.objects.get(pk=item_id)   
        Watchlist.objects.filter(user=request.user).filter(listing=item).delete()
    return HttpResponseRedirect(reverse("watchlist"))


#Bid on an item
@login_required(redirect_field_name=None, login_url="/login")
def bid(request, listing_id):
    #Get the bid value
    bid = float(request.POST["bid"])
    
    #Pull out the record of the concerned listing
    details = Listing.objects.get(pk=listing_id) 
    
    #Set the current price of the listing to be the new highest bid   
    details.current_price = bid

    #Set the highest bidder and the bid amount
    details.highest_bidder = request.user
    details.bid = bid

    #Save the changes
    details.save()

    #Redirect to the listing page
    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))


#Close the bidding on an item
@login_required(redirect_field_name=None, login_url="/login")
def close(request, listing_id):
    #Get the listing record
    item = Listing.objects.get(pk=listing_id)

    #Set its status to deactivated
    item.status = "D"

    #Save the changes
    item.save()

    #Redirect to the listing page
    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id" : listing_id}))


#Lets the visitor to a listing add a comment
@login_required(redirect_field_name=None, login_url="/login")
def addcomment(request, listing_id):
    #Get the comment text
    detail = request.POST["comment"]

    #Get the details of the concerned listing
    item = Listing.objects.get(pk=listing_id)

    #Create a comment
    comment = Comment(user=request.user, listing=item, comment=detail)

    #Save the comment to the DB.
    comment.save()

    #Redirect to the listing page.
    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id" : listing_id}))


#Display all the categories
@login_required(redirect_field_name=None, login_url="/login")
def categories(request):
    #List of 2-tuples where first item is what is stored in the DB and second item is visible to the user.
    cat = [c for c in Listing.category.field.choices]

    return render(request, "auctions/categories.html", {
        "cat": cat
    })


#Get all listings that belong to a particular category
@login_required(redirect_field_name=None, login_url="/login")
def catlist(request, category):

    #Get all the listings which belong to the input category and have active status
    listings = list(Listing.objects.filter(category=category, status="A"))

    return render(request, "auctions/catlist.html", {
        "listings": listings, "category": category.capitalize()
    })


#View the profile of a user
@login_required(redirect_field_name=None, login_url="/login")
def profile(request, username):

    #Get the details for the username
    user = User.objects.get(username=username)

    #Handle post request
    view = None
    if request.method == "POST":
        #Which view is the user asking for?
        whichView = request.POST["view"]        
        
        if whichView == "listings":
            #If whchView stores "listings", get all the user's listings
            view = list(Listing.objects.filter(user=user))
        else:
            #If whichView stores "auctions", get all auctions where the user has won.
            view = list(Listing.objects.filter(highest_bidder=user))
    
        print(view)

    return render(request, "auctions/profile.html", {
        "profile": user, "view": view
    })
