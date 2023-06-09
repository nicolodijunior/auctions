from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.template.defaulttags import register
from .models import User, Listing, Categories, Bids, Comments, Watchlist
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib import messages


MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

class NewListingForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={"class" : "form-control"}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={"class" : "form-control"}))
    min_bid = forms.FloatField(label="Minimum Bid", widget=forms.TextInput(attrs={"class" : "form-control"}))
    img_path = forms.CharField(label="Image source", widget=forms.TextInput(attrs={"class" : "form-control"}))

@login_required(login_url="/login")
def new_listing(request):
    if request.method == "POST":
        # objects
        current_user = request.user
        category = Categories.objects.get(pk=int(request.POST["category"]))
        # simple fields
        title = request.POST["title"]
        description = request.POST["description"]
        min_bid = float(request.POST["min_bid"])
        status = True
        img_path = request.POST["img_path"]        
        l = Listing(user=current_user, title=title, description=description, min_bid=min_bid, status=status, img_path=img_path, category=category)
        l.save()
        return HttpResponseRedirect(reverse("listing", args=(l.id,)))

    else:
        categories = Categories.objects.all()
        return render(request, "auctions/new_listing.html", {
            "categories": categories,
            "new_listing_form": NewListingForm()
        })


@register.filter(name="get_best_bid")
def get_best_bid(dictionary, key):
    return f"${dictionary.get(key):,.2f}"

@register.filter(name="add_to_watchlist")
def add_to_watchlist(request, listing_id):
    user = request.user   

    #accessing listing object
    listing = Listing.objects.get(pk=listing_id)
    is_there = False
    # check if the listing is on the user watchlist only if the user is logged in
        # LOADING USER WATCHLIST VALUES
        # user should have one watchlist, so we access it and check if it already exists
    w = user.user_watchlists.first()
    
    if w == None:
        # if it does not exist we need to know so we are sure that the listing is not in the watchlist and we can show the add to watchlist button
        w = Watchlist(user=user)     
        w.save()
        w.listings.add(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    else:
        # if it exists, we need to check if this listing is in the watchlist already to show the remove button
        for l in w.listings.all():
                if l == listing:
                    # check if listing is on user watchlist
                    is_there = True
    if is_there == True:
        #listing is already on the watchlist
        message = "Listing already on watchlist"
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    else:
        w.listings.add(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    

def remove_from_watchlist(request, listing_id):
    if request.method == "POST":
        user = request.user   
        listing = Listing.objects.get(pk=listing_id)
        w = user.user_watchlists.first()
        w.listings.remove(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def my_watchlist(request):
    user = request.user
    watchlists = user.user_watchlists.all
    return render(request,"auctions/my_watchlist.html", {
        "watchlists": watchlists,
    })

def make_bid(request, listing_id):
    if request.method=="POST":
        current_user = request.user
        listing = Listing.objects.get(pk=listing_id)
        bids = listing.listing_bids.all()
        user_bid = float(request.POST["bid"])
        biggest = True
        for bid in bids:
            if (user_bid <= bid.amount):
                biggest = False
                # checking if this is a valid bid
        if biggest:
            # if the amount the user wants to bid is enough he can make the bid
            b = Bids(owner=current_user,listing=listing,amount=user_bid)
            b.save()
            messages.success(request, 'Bid made successfully.')
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
        else:
            messages.error(request, 'Bid not made, please check the minimum bid.')
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
            
        #return HttpResponseRedirect(reverse("listing", args=(listing.id)), {"mesage": "You made a bid"})

def index(request):
    # listing receives all listings active
    listings = Listing.objects.filter(status=True)
    best_bids = {}
    # for each listing, check the maximum bid and storing it in a way it is easy to output
    for listing in listings:
        bids = listing.listing_bids.all()
        if not bids or bids==None:
            best_bids[listing.id] = listing.min_bid 
        biggest_bid = 0.000
        for bid in bids:
            bid = float(bid.amount)
            if bid > biggest_bid:
                biggest_bid = bid
            best_bids[listing.id] = biggest_bid
    
    #send listing with its best bid to index so it is possible to display it
    return render(request, "auctions/index.html", {
        "listings": listings,
        "best_bids": best_bids,
    })

def end_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.status=False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def listing(request, listing_id):
    
    # INFORMATIONS NEEDED IN THIS VIEW
    # saving user as user
    user = request.user   

    #accessing listing object
    listing = Listing.objects.get(pk=listing_id)
    is_there = False
    is_owner = False
    # CHECK IF USER OWNS THE BID
    if listing.user == user:
        is_owner = True
    # check if the listing is on the user watchlist only if the user is logged in
    if user.is_authenticated:
        # LOADING USER WATCHLIST VALUES
        # user should have one watchlist, so we access it and check if it already exists
        w = user.user_watchlists.first()
        
        if w == None:
            # if it does not exist we need to know so we are sure that the listing is not in the watchlist and we can show the add to watchlist button
            is_there = False
        else:
            # if it exists, we need to check if this listing is in the watchlist already to show the remove button
            for l in w.listings.all():
                    if l == listing:
                        # check if listing is on user watchlist
                        is_there = True

    # LOADING CURRENT PRICE INFORMATION
    # checking all bids of the listing
    bids = listing.listing_bids.all()

    # creating a best_bids with value zero
    best_bid = 0.00

    # checking if there is no bid, and if it is not, saving the minimum amount as best_bid to be displayed as current value of the listing
    if not bids or bids==None:
        best_bid = listing.min_bid
    
    is_winner = False
    bidowner = ""
    # comparing the bids to save the biggest value
    for bid in bids:
        if (listing.min_bid < float(bid.amount) > best_bid) :
            best_bid = float(bid.amount)
            bidowner = bid.owner.username
        else:
            best_bid = listing.min_bid
    
    if bidowner == user.username:
        is_winner = True

    
    comments = listing.listing_comments.all()

    # returning alues needed to the template
    return render(request, "auctions/listing.html", {
        "is_owner": is_owner,
        "is_there": is_there,
        "listings": listing,
        "best_bid": f"${best_bid:,.2f}",
        "is_winner": is_winner,
        "comments": comments,
    })
@register.filter(name="mmake_comment")
def make_comment(request, listing_id):
    if request.method == "POST":
        current_user = request.user
        listing = Listing.objects.get(pk=listing_id)
        c = request.POST["text_comment"]
        now = datetime.datetime.now()
        com = Comments(user=current_user,listing=listing,date_time=now, comment=c)
        com.save()
        # return HttpResponse("Until here, fine")
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    else:
        return HttpResponse("Should not be get")

def category_listings(request, category_name):
    category = Categories.objects.get(name=category_name)
    listings = category.category_listings.all()
    return render(request, "auctions/category_listings.html",{
        "listings": listings,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username,password=password)

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

def categories(request):
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })