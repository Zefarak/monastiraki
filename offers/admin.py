from django.contrib import admin
from .models import Offer, OfferItem


class OfferItemInline(admin.TabularInline):
    model = OfferItem
    fields = ['product_related', 'offer_related',]
    autocomplete_fields = ['product_related']
    readonly_fields = []


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'offer_value', 'active']
    list_filter = ['active']
    inlines = [OfferItemInline]


