from django.contrib.auth.models import AbstractUser
from django.db import models

#Store each individual user to the website
class User(AbstractUser):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)


"""Store all the listings created by the users. There is a one-to-many
relationship between User and Listing"""
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    starting_bid = models.IntegerField()
    current_price = models.IntegerField(default = starting_bid)
    image_url = models.URLField(default="No image provided")
    state = [("A", "Active"), ("D", "Deactive")]
    status = models.CharField(max_length=8, choices=state, default="A")
    CATEGORY_CHOICES = [
        ("ANTIQUES", "Antiques"),
        ("AUTOMOTIVE", "Automotive"),
        ("BOOKS", "Books/Textbooks",), 
        ("ELECTRONICS", "Electronics",), 
        ('FASHION', "Fashion",), 
        ("TOYS", "Toys",), 
        ("HOME", "Home/Kitchen",),
        ]
    category = models.CharField(
        max_length=64,
        choices=CATEGORY_CHOICES,
        default="Not Provided"
    )
    highest_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", blank=True, null=True)

    def __str__(self):
        return f"User: {self.user}, Product: {self.title}, Current Price: {self.current_price}, Highest Bidder: {self.highest_bidder}"


#Comments made on a particular listing
class Comment(models.Model):
    #User who made the comment
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    #Listing on which the comment was made
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings")

    #The content of the comment
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return f"User: {self.user}, Listing: {self.listing}, Comment: {self.comment}"


#Stores the listings each user has watchlisted
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlistuser")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlistitem")
