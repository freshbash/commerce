from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    starting_bid = models.IntegerField()
    current_price = models.IntegerField(default = 0)
    image_url = models.URLField(default="No image provided")
    state = [("A", "Active"), ("D", "Deactive")]
    status = models.CharField(max_length=8, choices=state, default="A")
    CATEGORY_CHOICES = [
        ("ANTIQUES", "Antiques"),
        ("AUTOMOBILES", "Automobiles"),
        ("BOOKS", "Books/Textbooks",), 
        ("ELECTRONICS", "Electronics",), 
        ('FASHION', "Fashion",), 
        ("TOYS", "Toys",), 
        ("HOME", "Home/Kitchen",),
        ]
    category = models.CharField(
        max_length=64,
        choices=CATEGORY_CHOICES,
        default=""
        )

    def __str__(self):
        return f"User: {self.user}, Product: {self.title}, Current Price: {self.current_price}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.IntegerField()

    def __str__(self):
        return f"User: {self.user}, Listing: {self.listing}, Bid: {self.bid}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings")
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return f"User: {self.user}, Listing: {self.listing}, Comment: {self.comment}"
