from django.contrib import admin

from .models import Room

# This line tells the admin site to manage Room objects.
admin.site.register(Room)
