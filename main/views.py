from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Listing
from .forms import ListingForm
from users.forms import LocationForm

# Create your views here.
def main_view(request):
  return render(request, "views/main.html", {"name": "AutoMax"})

@login_required
def home_view(request):
  listings = Listing.objects.all()
  context= {
    'listings': listings,
  }
  return render(request, "views/home.html", context)

@login_required
def list_view(request):
  if request.method == 'POST':
    pass
  elif request.method == 'GET':
    listing_form = ListingForm()
    location_form = LocationForm()
  return render(request, "views/list.html", {'listing_form': listing_form, 'location_form': location_form})