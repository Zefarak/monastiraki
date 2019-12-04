from django.db import models


class ProductSiteQuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(active=True, site_active=True)
        
    def category_queryset(self, cate):
        # pass list of categories, used on CategoryView
        return self.active().filter(category_site__in=cate)


class ProductManager(models.Manager):

    def active(self):
        return super(ProductManager, self).filter(active=True)

    def active_for_site(self):
        return self.active().filter(site_active=True)

    def active_with_qty(self):
        return self.active_for_site().filter(qty__gte=0)

    def get_site_queryset(self):
        return ProductSiteQuerySet(self.model, using=self._db)

    def featured_products(self):
        return self.active_for_site().filter(is_featured=True)

