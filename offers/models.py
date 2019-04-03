from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.core.cache import cache
from products.models import Product
from .tools import check_size, upload_location
CURRENCY = settings.CURRENCY


class Offer(models.Model):
    active = models.BooleanField(default=True, verbose_name='Status')
    image = models.ImageField(blank=True,
                              validators=[FileExtensionValidator(['jpg', 'png']),
                                          check_size
                                          ],
                              upload_to=upload_location,
                              help_text='600*400'
                              )
    front_page = models.BooleanField(default=True, verbose_name='Εμφανίσιμο στην αρχικη σελίδα')
    title = models.CharField(unique=True, max_length=200, verbose_name='Τίτλος')
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Αρχίκη Αξία')
    offer_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Εκπτωτική Αξία')
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        # there is a signal on the bottom of the page for creating slug
        self.value = self.offer_items.all().aggregate(Sum('value'))['value__sum'] if self.offer_items.all() else 0
        super(Offer, self).save(*args, **kwargs)
        cache.delete('cache_offer_queryset')

    def tag_value(self):
        return f'{self.value} {CURRENCY}'

    def tag_offer_value(self):
        return f'{self.offer_value} {CURRENCY}'

    def get_absolute_url(self):
        return reverse('offer_detail_view', kwargs={'slug': self.slug})


class OfferItem(models.Model):
    offer_related = models.ForeignKey(Offer, related_name='offer_items', on_delete=models.CASCADE)
    product_related = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        return f'{self.product_related.title}'

    def save(self, *args, **kwargs):
        self.value = self.product_related.final_price
        super(OfferItem, self).save(*args, **kwargs)
        self.offer_related.save()


@receiver(post_save, sender=Offer)
def create_slug_name(sender, instance, **kwargs):
    if not instance.slug:
        slug = slugify(instance.title, allow_unicode=True)
        qs_exists = Offer.objects.filter(slug=slug).exists()
        if qs_exists:
            slug = f'{slug}-{instance.id}'
        instance.slug = slug
        instance.save()
