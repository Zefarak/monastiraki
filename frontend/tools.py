from django.core.cache import cache
from frontend.models import CategorySite, Brand


def initial_data(request):
    categories_cache = cache.get('cache_nav_cate', 'has_expired')
    if categories_cache == 'has_expired':
        cache.add('cache_nav_cate', CategorySite.my_query.navbar())
    menu_categories = cache.get('cache_nav_cate')
    cart, cart_items = '', ''
    return menu_categories, cart, cart_items


def initial_filter_data(queryset):
    brands_id = queryset.values_list('brand', flat=False)
    brands = Brand.objects.filter(id__in=brands_id)
    categories_id = queryset.values_list('category_site', flat=False)
    categories = CategorySite.objects.filter(id__in=categories_id)
    return [brands, categories]


def category_filter_data(queryset, cate_id):
    cache_brands = cache.get(f'category_filter_brands_{cate_id}', 'has_expired')
    if cache_brands == 'has_expired':
        brands_id = queryset.values_list('brand', flat=False)
        brands = Brand.objects.filter(id__in=brands_id)
        cache.add(f'category_filter_brands_{cate_id}', brands)
        cache_brands = brands

    cache_categories = cache.get(f'category_filter_cate_{cate_id}', 'has_expired')
    if cache_categories == 'has_expired':
        print('first step')
        categories_id = queryset.values_list('category_site', flat=False)
        categories = CategorySite.objects.filter(id__in=categories_id).exclude(id=cate_id)
        if categories:
            print('second')
            cache.add(f'category_filter_cate_{cate_id}', categories)

        cache_categories = categories
    print(cache_categories)
    return [cache_brands, cache_categories]


def grab_user_filter_data(request):
    brand_name = request.GET.getlist('brand_name')
    category_name = request.GET.getlist('site_cate_name')
    return [brand_name, category_name]

