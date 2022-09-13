from imp import reload
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

from .models import Listing, LikedListing
from .forms import ListingForm
from users.forms import LocationForm
from .filters import ListingFilter

# Create your views here.
def main_view(request):
  return render(request, "views/main.html", {"name": "AutoMax"})

@login_required
def home_view(request):
  listings = Listing.objects.all()
  listing_filter = ListingFilter(request.GET, queryset=listings)
  user_liked_listings = LikedListing.objects.filter(profile=request.user.profile).values_list('listing')
  liked_listings_ids = [ l[0] for l in user_liked_listings ]
  context= {
    'listing_filter': listing_filter,
    'liked_listings_ids': liked_listings_ids,
  }
  return render(request, "views/home.html", context)

@login_required
def list_view(request):
  if request.method == 'POST':
    try:
      listing_form = ListingForm(request.POST, request.FILES)
      location_form = LocationForm(request.POST)
      if listing_form.is_valid() and location_form.is_valid():
        listing = listing_form.save(commit=False)
        listing_location = location_form.save()
        listing.seller = request.user.profile
        listing.location = listing_location
        listing.save()
        messages.info(request, f'{listing.model} Listing Posted Successfully!')
        return redirect('home')
      else:
        raise Exception()
    except Exception as e:
      messages.error(request, 'An error occured while posting the listing.')
  elif request.method == 'GET':
    listing_form = ListingForm()
    location_form = LocationForm()
  return render(request, "views/list.html", {'listing_form': listing_form, 'location_form': location_form})

@login_required
def listing_view(request, id):
  try:
    listing = Listing.objects.get(id=id)
    if listing is None:
      raise Exception
    return render(request, 'views/listing.html', {'listing': listing})
  except Exception as e:
    messages.error(request, f'Invalid UID {id} was provided for listing.')
    return redirect('home')

@login_required
def edit_view(request, id):
  try:
    listing = Listing.objects.get(id=id)
    if listing is None:
      raise Exception()
    if request.method == 'POST':
      listing_form = ListingForm(request.POST, request.FILES, instance=listing)
      location_form = LocationForm(request.POST, instance=listing.location)
      if listing_form.is_valid() and location_form.is_valid():
        listing_form.save()
        location_form.save()
        messages.info(request, f'Listing {id} is updated successfully!')
        return redirect('home')
      else:
        messages.error(request, f'An error occurred while trying to edit the listing.')
        # return reload()
        pass
    else:
      listing_form = ListingForm(instance=listing)
      location_form = LocationForm(instance=listing.location)
    context = {
      'listing_form': listing_form, 
      'location_form': location_form
    }
    return render(request, 'views/edit.html', context)
  except Exception as e:
    messages.error(request, f'An error occurred while trying to access the edit page.')
    return redirect('home')
  
@login_required
def like_listing_view(request, id):
  listing = get_object_or_404(Listing, id=id)

  liked_listing, isCreated = LikedListing.objects.get_or_create(profile=request.user.profile, listing=listing)

  if not isCreated:
    # dislike - unlike
    liked_listing.delete()
  else:
    liked_listing.save()

  return JsonResponse({
    'is_liked_by_user': isCreated,
  })

@login_required
def inquire_listing_using_email(request, id):
  listing = get_object_or_404(Listing, id=id)
  try:
    email_subject = f'{request.user.username} is interested in {listing.model}'
    email_message = f'Hi, {listing.seller.user.username}, {request.user.username} is interested in your {listing.model} listing on AutoMax'
    send_mail(email_subject, email_message, 'noreply@automax.com', [listing.seller.user.email, ], fail_silently=True)
    return JsonResponse({
      "success": True,
    })
  except Exception as e:
    print(e)
    return JsonResponse({
      'success': False,
      'info': e,
    })