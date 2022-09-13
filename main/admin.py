from django.contrib import admin

from main.models import Listing, LikedListing

class ListingAdmin(admin.ModelAdmin):
  readonly_fields = ('id',)

class LikedListingAdmin(admin.ModelAdmin):
  readonly_fields = ('id', 'liked_date')


# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(LikedListing, LikedListingAdmin)