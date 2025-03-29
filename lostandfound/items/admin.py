from django.contrib import admin
from .models import LostItem, Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'building', 'floor', 'room')

@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'category', 'lost_location', 'found_location', 'lost_time', 'found_time')
    list_filter = ('status', 'category', 'lost_time', 'found_time')
    search_fields = ('title', 'description', 'category')