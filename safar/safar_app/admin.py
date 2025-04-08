from django.contrib import admin

# Register your models here.
from .models import Destination, Trip, Itinerary

admin.site.register(Destination)
admin.site.register(Trip)
admin.site.register(Itinerary)