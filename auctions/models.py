from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    # watchlists = models.foreignKey(Watchlist, on_delete=models.CASCADE, related_name="watchlist user", verbose_name="Watchlists of the user")

class Categories(models.Model):
  name = models.CharField(max_length=32, verbose_name="Categories of listings.")



class Listing(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings", verbose_name="User that made this listing.")
  title = models.CharField(max_length=64, verbose_name="Title of the listing")
  description = models.CharField(max_length=64, verbose_name="Description of the listing.")
  min_bid = models.FloatField(verbose_name="Minimum bid allowed for this bid.")
  status = models.BooleanField(verbose_name="Status, active of inactive, true or false")
  img_path = models.CharField(max_length=256, verbose_name="Link of the listing image, took from the web")
  category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="category_listings", verbose_name="Category of the listing.")

class Bids(models.Model):
  # The bids made in various auctions
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids", verbose_name="Who made the bid.")
  listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids", verbose_name="From which listing this bid is.")
  amount = models.FloatField(verbose_name="Amount in usd of this bid.")


class Comments(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments", verbose_name="User who made the comments.")
  listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments", verbose_name="The listing the comment is about.")
  date_time = models.DateTimeField(auto_now=True)
  comment = models.CharField(max_length=256, verbose_name="Comment")

class Watchlist(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlists", verbose_name="User who created the watchlist.")
  listings = models.ManyToManyField(Listing, blank=True, related_name="listing_watchtlists", verbose_name="All listings of the watchlist.")

"""
(OK)Auction Listings
  Description: This is more like a product
  Fields: id(OK), user_id(OK), Title(OK), description(OK), value of starting bid(OK), image url(OK), status - active or inactive(OK)

(OK) Bids
 São os lances dados em cada produto, me lembra um pouco o histórico de compras das ações de finance50
 Fields: id(OK), user_id(OK), listing_id(OK), amount(OK)

Comments
 São comentários listados nos produtos, ou, Auction Listings como se chama aqui
 Fields: user_id, listing_d, data e hora do comentário


(OK)Categories
 Categorias dos produtos, para que o usuário possa consultar por categorias.
 Fields: categoryid(OK) and name of the categorie (OK)

Watchlist
 Lista de desejos
 Fields: user_id, auction_id



"""
# TABLES: auction_listings(product), bids, comments, categories
