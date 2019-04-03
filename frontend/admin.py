from django.contrib import admin
from django.core.cache import cache
from django.db.models import Count
from .models import Banner, CategorySite, Brand
from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin
from .actions import *


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['tag_image', 'title', 'active']
    fields = ['active', 'title', 'tag_image', 'image', 'href', 'text', 'new_window']
    list_filter = ['active']
    readonly_fields = ['tag_image']
    actions = [active, deactive]
    list_per_page = 10


@admin.register(CategorySite)
class CategorySiteAdmin(ImportExportModelAdmin, DraggableMPTTAdmin):
    list_display = ['tree_actions', 'indented_title', 'show_on_menu', 'active', 'cate_count']
    list_display_links = ['indented_title', ]
    list_filter = ['active', 'show_on_menu', 'order']
    search_fields = ['name']
    autocomplete_fields = ['parent']
    actions = [active, deactive, activeOnBar, create_missing_slug, reset_cache_action]
    list_per_page = 100

    def cate_count(self, obj):
        return obj._cate_count

    cate_count.admin_order_field = '_cate_count'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_cate_count=Count('products', distinct=True))
        return queryset


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_filter = ['active']
    search_fields = ['title']
    actions = [reset_brand_cache_action, ]
    list_display = ['title', 'active']
    readonly_fields = ['tag_image', ]
    fields = ['active', 'title', 'tag_image', 'image', 'slug', 'meta_description' ]