from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse
from .models import Banner, CategorySite
from model_mommy import mommy


class CategotyTest(TestCase):

    def create_category(self, title='Shoes', parent=None):
        return CategorySite.objects.create(title=title,
                                           parent=parent)

    def create_banner(self,):
        return Banner.objects.create()

    def test_category_creation(self):
        w = self.create_category()
        b = self.create_banner()
        self.assertTrue(isinstance(b, Banner))
        self.assertTrue(isinstance(w, CategorySite))
        self.assertEqual(w.__str__(), w.title)


class FrontEndTestCase(TestCase):

    def setUp(self):
        bannner_1 = mommy.make(Banner)
        bannner_2 = mommy.make(Banner)
        bannner_3 = mommy.make(Banner)
        cate_1 = mommy.make(CategorySite)
        cate_2 = mommy.make(CategorySite)
        cate_3 = mommy.make(CategorySite)

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_offer_page(self):
        response = self.client.get(reverse('offers_page'))
        self.assertEqual(response.status_code, 200)