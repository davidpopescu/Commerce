from django.contrib import admin
from .models import auctionListing, Bid, Comment, watchList
# Register your models here.

admin.site.register(auctionListing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(watchList)