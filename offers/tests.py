from django.test import TestCase
from .models import Offer, OfferItem, Product


class OfferTestCase(TestCase):

    def setUp(self):
        new_product = Product.objects.create(title='Coca Cola', price=2)
        self.my_cola = Offer.objects.create(title='cola coca')
        Offer.objects.get_or_create(title='cola coca')
        self.first_item = OfferItem.objects.get_or_create(offer_related=self.my_cola,
                                                          product_related=new_product
                                                          )

    def test_offers_create_slug(self):
        coca_cola = Offer.objects.get(title='cola coca')
        self.assertEqual(coca_cola.slug, 'cola-coca')

    def test_calculate_value(self):
        self.assertEqual(self.my_cola.value, 2.00)



