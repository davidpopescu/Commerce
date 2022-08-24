from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class auctionListing(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    category = models.CharField(max_length=20)
    details = models.CharField(max_length = 1000)
    price = models.IntegerField()
    ending_date = models.DateField()
    image = models.ImageField(upload_to = 'images')
    ended = models.BooleanField(default = False)
    winner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "winner")
    def __str__(self):
        return f"{self.name} - {self.category}"
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    bid_amount = models.IntegerField()
    update_date = models.DateField()

    def __str__(self):
        return f"{self.user} - {self.bid_amount}"
        
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    listing = models.ForeignKey(auctionListing, on_delete = models.CASCADE)
    comment = models.TextField()
    update_date = models.DateField(auto_now_add = True)

    def __str__(self):
        return f"{self.user} - {self.listing}"

class watchList(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    listing = models.ForeignKey(auctionListing, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.listing}"

