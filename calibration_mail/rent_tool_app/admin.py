from django.contrib import admin
from .models import Device, Location

# Register your models here.
class Admin_location(admin.ModelAdmin):
    search_fields = ("country", "city")
    list_display = ("country","city")
    #readonly_fields = ("calibration_required")


class Admin_device(admin.ModelAdmin):
    #readonly_fields = ("created", "updated")
    search_fields = ("name", "is_available")
    list_display = ("name","is_available")

admin.site.register(Location, Admin_location)
admin.site.register(Device, Admin_device)

