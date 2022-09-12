from django.contrib import admin

from main.models import Listing

class ListingAdmin(admin.ModelAdmin):
  readonly_fields = ('id',)

# Register your models here.
admin.site.register(Listing, ListingAdmin)