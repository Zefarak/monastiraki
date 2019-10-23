from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from frontend.models import CategorySite


class StaticViewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return ['homepage', 'offers_page', 'categories_list', 'brands_list', 'about_page']

    def location(self, obj):
        return reverse(obj)


class CategorySiteSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return CategorySite.objects.filter(active=True)
