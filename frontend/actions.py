from django.core.cache import cache


def create_missing_slug(modeladmin, request, queryset):
    for ele in queryset:
        ele.save()


create_missing_slug.short_description = 'Δημιουργία slug'


def reset_cache_action(modeladmin, request, queryset):
    for ele in queryset:
        cache.delete(f'cache_generate_cate_ancestors_{ele.id}')
        cache.delete(f'cache_cate_queryset_{ele.id}')
        cache.delete(f'category_filter_brands_{ele.id}')
        cache.delete(f'category_filter_cate_{ele.id}')
    cache.delete('cache_nav_cate')
    cache.delete('cache_categories')


reset_cache_action.short_description = 'Διαγραφή cache κατηγοριών'


def reset_brand_cache_action(modeladmin, request, queryset):
    for ele in queryset:
        cache.delete(f'brand_detail_{ele.id}')
    cache.delete('brand_list')


reset_brand_cache_action.short_description = 'Εκαθάριση Cache'


def active(modeladmin, request, queryset):
    queryset.update(active=True)


active.short_description = "Ενεργοποίηση"


def deactive(modeladmin, request, queryset):
    queryset.update(active=False)


deactive.short_description = "Απενεργοποίηση"


def activeOnBar(modeladmin, request, queryset):
    queryset.update(show_on_menu=False)


activeOnBar.short_description = "Απενεργοποίηση από Navbar"




