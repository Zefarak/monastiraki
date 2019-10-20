from django.contrib import admin

from .models import Leaflet


@admin.register(Leaflet)
class LeafletAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']
    search_fields = ['title']
