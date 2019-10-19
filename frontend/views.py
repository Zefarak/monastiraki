from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, TemplateView
from django.core.cache import cache
from .models import Banner, Brand
from products.models import Product, CategorySite
from offers.models import Offer
from .mixins import SearchMixin, custom_redirect
from .tools import initial_data, initial_filter_data, grab_user_filter_data, category_filter_data
from django.http import JsonResponse
from django.template.loader import render_to_string


class HomepageView(SearchMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        cache_banners = cache.get('cache_banners', 'has_expired')
        if cache_banners == 'has_expired':
            cache.add('cache_banners', Banner.objects.filter(active=True))
        banners = cache_banners if cache_banners != 'has_expired' else cache.get('cache_banners', 'has_expired')
        menu_categories, cart, cart_items = initial_data(self.request)
        context.update(locals())
        return context


class OffersPageView(SearchMixin, ListView):
    model = Product
    template_name = 'product_list.html'
    paginate_by = 6
    queryset = Offer.objects.filter(active=True)

    def get_queryset(self):
        cache_queryset = cache.get('cache_offer_queryset', 'has_expired')
        if cache_queryset == 'has_expired':
            cache.add('cache_offer_queryset', Product.my_query.active_for_site().filter(price_discount__gt=0))
        queryset = Product.my_query.active_for_site().filter(price_discount__gt=0)
        queryset = Product.filters_data(self.request, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(OffersPageView, self).get_context_data(**kwargs)
        menu_categories, cart, cart_items = initial_data(self.request)
        if 'search_name' in self.request.GET:
            search_name = self.request.GET.get('search_name')
            return custom_redirect('search_page', search_name=search_name)
        seo_title = 'Μικρο Μοναστηράκι | Προσφορές'
        context.update(locals())
        return context


def offer_detail_view(request, slug):
    instance = get_object_or_404(Offer, slug=slug)
    menu_categories, cart, cart_items = initial_data(request)
    if 'search_name' in request.GET:
        search_name = request.GET.get('search_name')
        return custom_redirect('search_page', search_name=search_name)
    context = locals()
    return render(request, 'offer_detail.html', context)


class CategoriesPageListView(SearchMixin, ListView):
    template_name = 'categories.html'
    paginate_by = 10
    model = CategorySite

    def get_queryset(self):
        my_cache = cache.get('cache_categories', 'has_expired')
        if my_cache == 'has_expired':
            cache.add('cache_categories', CategorySite.my_query.main_page_show())
        queryset = my_cache if my_cache != 'has_expired' else cache.get('cache_categories')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoriesPageListView, self).get_context_data(**kwargs)
        menu_categories, cart, cart_items = initial_data(self.request)
        seo_title = 'Οι κατηγορίες μας'
        context.update(locals())
        return context


class CategoryListDetailView(ListView):
    template_name = 'categories.html'
    paginate_by = 10
    model = CategorySite

    def get_queryset(self):
        self.category = get_object_or_404(CategorySite, slug=self.kwargs['slug'])
        queryset = CategorySite.objects.filter(parent=self.category, active=True).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryListDetailView, self).get_context_data(**kwargs)
        menu_categories, cart, cart_items = initial_data(self.request)
        seo_title = f'{self.category.name}'
        title = self.category.name
        context.update(locals())
        return context


class CategoryDetailView(SearchMixin, ListView):
    template_name = 'product_list.html'
    model = Product
    paginate_by = 15

    def get_queryset(self):
        self.category = get_object_or_404(CategorySite, slug=self.kwargs['slug'])

        '''
        generate_ancestors = cache.get(f'cache_generate_cate_ancestors_{self.category.id}', 'has_expired')
        if generate_ancestors == 'has_expired':
            generate_ancestors = cache.add(f'cache_generate_cate_ancestors_{self.category.id}',
                                           self.category.get_childrens_and_grandchilds()
                                           )
            family = self.category.get_childrens_and_grandchilds()|CategorySite.objects.filter(id=self.category.id)
        else:
            family = generate_ancestors|CategorySite.objects.filter(id=self.category.id)
        '''

        queryset = cache.get(f'cache_cate_queryset_{self.category.id}', 'has_expired')
        if queryset == 'has_expired':
            queryset = Product.objects.filter(category_site=self.category).distinct()
            cache.set(f'cache_cate_queryset_{self.category.id}', queryset)

        queryset = Product.filters_data(self.request, queryset)
        queryset = Product.queryset_ordering(self.request, queryset)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        seo_title, page_title = f'Μοναστηράκι | {self.category.name}', f'Έχετε επιλέξει την κατηγορία {self.category}'
        menu_categories, cart, cart_items = initial_data(self.request)
        brands, categories = category_filter_data(self.object_list, self.category.id)
        brand_name, cate_name = grab_user_filter_data(self.request)
        title = self.category.name
        context.update(locals())
        return context


class SearchPageView(ListView):
    model = Product
    template_name = 'search_list.html'
    paginate_by = 6

    def get_queryset(self):
        search_name = self.request.GET.get('search_name', None)
        queryset = Product.objects.none()
        if search_name:
            queryset = Product.my_query.active_for_site() if len(search_name) > 2 else Product.objects.none()
        queryset = Product.filters_data(self.request, queryset)
        queryset = Product.queryset_ordering(self.request, queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(SearchPageView, self).get_context_data(**kwargs)
        page_title = 'Απότελέσμα της αναζήτησης %s' % self.request.GET.get('search_name', '-')
        menu_categories, cart, cart_items = initial_data(self.request)
        brands, categories = initial_filter_data(self.object_list)
        brand_name, cate_name= grab_user_filter_data(self.request)
        seo_title = '%s' % self.search_name
        search_name = self.request.GET.get('search_name', None)
        context.update(locals())
        return context

    def get(self, *args, **kwargs):
        self.search_name = self.request.GET.get('search_name', None)
        return super(SearchPageView, self).get(*args, **kwargs)


class ContactPageView(SearchMixin, TemplateView):
    template_name = 'contact_page.html'

    def get_context_data(self, **kwargs):
        context = super(ContactPageView, self).get_context_data(**kwargs)
        menu_categories, cart, cart_items = initial_data(self.request)
        context.update(locals())
        return context


class BrandListView(SearchMixin, ListView):
    template_name = 'brand_page.html'
    model = Brand

    def get_queryset(self):
        cache_queryset = cache.get('brands_list', 'has_expired')
        if cache_queryset == 'has_expired':
            cache.add('brands_list', Brand.objects.filter(active=True))
        queryset = cache_queryset if cache_queryset != 'has_expired' else cache.get('brands_list')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(BrandListView, self).get_context_data(**kwargs)
        menu_categories, cart, cart_items = initial_data(self.request)
        context.update(locals())
        return context


class BrandDetailView(ListView):
    template_name = 'product_list.html'
    model = Product

    def get_queryset(self):
        self.brand = brand = get_object_or_404(Brand, slug=self.kwargs['slug'])
        cache_queryset = cache.get(f'brand_detail_{brand.id}', 'has_expired')
        if cache_queryset == 'has_expired':
            add_queryset = Product.my_query.active_for_site().filter(brand=brand)
            cache.add(f'brand_detail_{brand.id}', add_queryset)
        queryset = cache_queryset if cache_queryset != 'has_expired' else cache.get(f'brand_detail_{brand.id}')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(BrandDetailView, self).get_context_data(**kwargs)
        seo_title, page_title = f'Μοναστηράκι | {self.brand.title}', f'Έχετε επιλέξει την κατηγορία {self.brand}'
        menu_categories, cart, cart_items = initial_data(self.request)
        brands, categories = category_filter_data(self.object_list, self.brand.id)
        brand_name, cate_name = grab_user_filter_data(self.request)
        context.update(locals())
        return context


def ajax_search_brands(request):
    brands = Brand.filters_data(Brand.objects.filter(active=True), request)
    data = dict()
    data['result'] = render_to_string(request=request,
                                      template_name='ajax/container_result.html',
                                      context={
                                        'object_list': brands
                                      })

    return JsonResponse(data)


def ajax_search_categories(request):
    categories = CategorySite.filter_data(CategorySite.objects.filter(active=True), request)
    data = dict()
    data['result'] = render_to_string(request=request,
                                      template_name='ajax/categories_container.html',
                                      context={
                                          'object_list': categories
                                      })
    return JsonResponse(data)