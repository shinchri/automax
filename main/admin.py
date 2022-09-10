from django.contrib import admin

from main.models import Listing

class ListingAdmin(admin.ModelAdmin):
  pass

# Register your models here.
admin.site.register(Listing, ListingAdmin)