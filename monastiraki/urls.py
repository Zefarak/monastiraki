from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static


from frontend.views import (HomepageView, CategoryListDetailView, OffersPageView,CategoryDetailView,
                            SearchPageView, ContactPageView, offer_detail_view,
                            CategoriesPageListView, BrandListView, BrandDetailView,
                            ajax_search_brands, ajax_search_categories
                            )

admin.site.site_header = 'Το Μικρό Μοναστηράκι'
admin.site.site_title = 'Το Μικρό Μοναστηράκι'
admin.site.index_title = 'Αρχική Σελίδα'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomepageView.as_view(), name='homepage'),
    path('gdpr/', include('gdpr.urls')),
    path('προσφορές/', OffersPageView.as_view(), name='offers_page'),
    path('προσφορές/<slug:slug>/', offer_detail_view, name='offer_detail_view'),
    url(r'^προϊοντα-κατηγορίας/(?P<slug>[-\w]+)/$', CategoryDetailView.as_view(), name='products'),
    path('κατηγορίες/', CategoriesPageListView.as_view(), name='categories_list'),
    path('brands/', BrandListView.as_view(), name='brands_list'),
    url(r'^brands/(?P<slug>[-\w]+)/$', BrandDetailView.as_view(), name='brands_detail'),
    url(r'^κατηγορία/(?P<slug>[-\w]+)/$', CategoryListDetailView.as_view(), name='category_page'),
    # path('κατηγορία/<slug:slug>/', CategoryPageListView.as_view(), name='category_page'),
    path('αναζήτηση/', SearchPageView.as_view(), name='search_page'),
    path('about-us/', ContactPageView.as_view(), name='about_page'),

    # ajax
    path('ajax/brand/search/', ajax_search_brands, name='ajax_search_brands'),
    path('ajax/categories/search/', ajax_search_categories, name='ajax_search_categories'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
