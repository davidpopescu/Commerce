from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
import datetime
from .models import User, auctionListing, Bid, Comment, watchList
from .forms import BidForm, createForm, CommentForm
from django.contrib.auth.decorators import login_required

def handler404(request, exception):
    return render(request, 'auctions/error404.html', status=404)

def error_404_view(request, exception):
    return render(request, "auctions/error404.html", status=404)

def index(request):
    actualTime = datetime.date.today
    return render(request, "auctions/index.html", {
        "auctions": auctionListing.objects.all().filter(ended = False),
        "actualTime": actualTime
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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_Listing(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "form": createForm(),
        })

    if request.method == "POST":
        form = createForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            name = form.cleaned_data["name"]
            category = form.cleaned_data["category"]
            details = form.cleaned_data["details"]
            price = form.cleaned_data["price"]
            ending_date = form.cleaned_data["ending_date"]
            image = form.cleaned_data["image"]
            if ending_date < datetime.date.today():
                return render(request, "auctions/create.html", {
                    "form": form,
                    "message": "Ending date must be in the future."
                })
            auctionListing.objects.create(name=name, category=category, details=details, price=price, ending_date=ending_date, image=image, user=user, winner = user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "message": "All fields are required.",
            })
    else:
        return render(request, "auctions/create.html") 

def bid(request, id):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    listing = auctionListing.objects.get(id=id)
    comments = Comment.objects.filter(listing=listing)
    request.session['id'] = id
    if listing.ending_date == datetime.date.today():
        Bid.objects.create(user=user,bid_amount=bid_amount, ending_date = datetime.date.today())
        auctionListing.objects.filter(id=id).update(price=bid_amount, winner = user)
    if auctionListing.objects.filter(ending_date = datetime.date.today()):
        return render(request, "auctions/bid.html", {
            "id": id,
            "listing": listing,
            "comments": comments
        })

    if request.method == "GET" and 'closed' in request.GET:
        return HttpResponseRedirect("auctions/closed")
    elif request.method == "GET":
        return render(request, "auctions/bid.html", {
            "id": id,
            "listing": listing,
            "form": BidForm(),
            "comments": comments
        })
    elif request.method == "POST" and 'button' in request.POST:
        watchList.objects.create(user=user, listing=listing)
        return HttpResponseRedirect("auctions/watchList")
    elif request.method == "POST":
        bid_amount = request.POST["bid_amount"] 
        if int(bid_amount) <= int(listing.price):
            return render(request, "auctions/bid.html", {
                "id": id,
                "listing": listing,
                "form": BidForm(),
                "message": "Bid amount must be higher than the current price."
            })
        
        return HttpResponseRedirect(reverse("index"), {
            "message": "Bid placed successfully."
        })
        
    else:
        return render(request, "auctions/bid.html")

def addwatchList(request,id):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    listing = auctionListing.objects.get(id=id)
    watchList.objects.create(user=user, listing=listing)
    return HttpResponseRedirect(reverse("bid", args=(id,)))

def watch(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    listings = watchList.objects.filter(user=user)
    if request.method == "GET":
        return render(request, "auctions/watchList.html", {
            "listings": listings
        })
    




def closed(request, id):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    auctionListing.objects.filter(id = id).update(ended = True)
    listing = auctionListing.objects.get(id=id)
    if request.method == "GET":
        return render(request, "auctions/closed.html", {
            "listing": listing
        })


def newComment(request,id):
    user = request.user
    listing = auctionListing.objects.get(id=id)
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "GET":
        return render(request, "auctions/newComment.html", {
            "form": CommentForm(),
            "listing": listing
        })
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            Comment.objects.create(user=user, listing = listing, comment = comment)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/newComment.html", {
                "listing": listing,
                "form": form     
            })
    else:
        return render(request, "auctions/newComment.html")
    
def category(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    listings = auctionListing.objects.all()
    if request.method == "GET":
        return render(request, "auctions/category.html", {
            "listings": listings
        })
    
    if request.method == "POST":
        category = request.POST["category"]
        return HttpResponseRedirect(reverse("categories", args=(category,)), {
            "listings": listings,
            "category": category
        })

def categories(request, category):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    listings = auctionListing.objects.filter(category=category)
    if request.method == "GET":
        return render(request, "auctions/categories.html", {
            "listings": listings,
            "category": category
        })