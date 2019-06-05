from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db import models
from django.db.models.signals import post_save
from django.core.cache import cache
from django.dispatch import receiver
from django.utils.text import slugify
from site_settings.models import DefaultBasicModel
from site_settings.constants import MEDIA_URL
from .validators import *
from mptt.models import MPTTModel, TreeForeignKey
from tinymce.models import HTMLField


class CategorySiteManager(models.Manager):

    def active_queryset(self):
        return super(CategorySiteManager, self).filter(active=True)

    def main_page_show(self):
        return super(CategorySiteManager, self).filter(active=True, parent__isnull=True)

    def navbar(self):
        return self.active_queryset().filter(show_on_menu=True)


class CategorySite(MPTTModel):
    active = models.BooleanField(default=True, verbose_name='Κατάσταση')
    name = models.CharField(max_length=50, unique=True, verbose_name='Τίτλος')
    image = models.ImageField(blank=True, null=True, upload_to=category_site_directory_path, help_text='600*600')
    content = models.TextField(blank=True, null=True)
    date_added = models.DateField(auto_now=True)
    meta_description = models.CharField(max_length=300, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.IntegerField(default=1)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True, max_length=50)
    show_on_menu = models.BooleanField(default=False, verbose_name='Εμφάνιση στην Navbar')
    my_query = CategorySiteManager()
    objects = models.Manager()

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'Κατηγορίες Site'

    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = slugify(self.name, allow_unicode=True)
            qs_exists = CategorySite.objects.filter(slug=new_slug).exists()
            if qs_exists:
                new_slug = f'{new_slug} - {self.id}'
            self.slug = new_slug
            self.save()
        super().save(*args, **kwargs)

    def have_children(self):
        childs = self.children.exists()
        return True if childs else False

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def image_tag(self):
        if self.image:
            return mark_safe('<img scr="%s%s" width="400px" height="400px" />'%(MEDIA_URL, self.image))
        return 'No image'

    def image_tag_tiny(self):
        if self.image:
            return mark_safe('<img scr="%s%s" width="100px" height="100px" />'%(MEDIA_URL, self.image))
    image_tag.short_description = 'Είκονα'

    def tag_active(self):
        return 'Is Active' if self.active else 'No active'

    def tag_show_on_menu(self):
        return 'Show' if self.show_on_menu else 'No Show'

    def get_absolute_url(self):
        return reverse('category_page', kwargs={'slug': self.slug})

    def get_childrens(self):
        childrens = CategorySite.my_query.active_queryset().filter(parent=self)
        return childrens

    def get_childrens_and_grandchilds(self):
        childrens_values = CategorySite.objects.filter(parent=self).values_list('id')
        grand_childrens = CategorySite.objects.filter(parent__id__in=childrens_values)
        return self.get_childrens()| grand_childrens

    def tag_parent(self):
        return f'{self.parent}' if self.parent else 'Parent'
    
    @staticmethod
    def filter_data(queryset, request):
        search_name = request.GET.get('search_name', None)
        queryset = queryset.filter(name__contains=search_name.capitalize()) if search_name else queryset
        return queryset


class Brand(models.Model):
    active = models.BooleanField(default=True, verbose_name='Ενεργοποίηση')
    title = models.CharField(max_length=120, verbose_name='Ονομασία Brand')
    image = models.ImageField(blank=True, upload_to='brands/', verbose_name='Εικόνα', help_text='600*600')
    order_by = models.IntegerField(default=1,verbose_name='Σειρά Προτεριότητας')
    meta_description =models.CharField(max_length=255, blank=True)
    width = models.IntegerField(default=240)
    height = models.IntegerField(default=240)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)

    class Meta:
        verbose_name_plural = 'Brands'
        ordering = ['title']

    def save(self, *args, **kwargs):
        cache.add(f'brand_detail_{self.id}', self.product_set.all().filter(active=True,
                                                                           site_active=True,
                                                                           brand__id=self.id)
                  )
        cache.add('brand_list', Brand.objects.filter(active=True))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def tag_image(self):
        return mark_safe('<img src="%s%s" width="200px" height="200px" />' % (MEDIA_URL, self.image))

    tag_image.short_description = 'Εικόνα'

    def tag_active(self):
        return 'Active' if self.active else 'No active'

    def get_absolute_url(self):
        return reverse('brands_detail', kwargs={'slug': self.slug})

    @staticmethod
    def filters_data(queryset, request):
        search_name = request.GET.get('search_name', None)
        active_name = request.GET.getlist('active_name', None)
        brand_name = request.GET.getlist('brand_name', None)
        queryset = queryset.filter(id__in=brand_name) if brand_name else queryset
        queryset = queryset.filter(title__contains=search_name.capitalize()) if search_name else queryset
        queryset = queryset.filter(active=True) if active_name else queryset
        return queryset


class FirstPage(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(unique=True, max_length=150)
    image = models.ImageField(upload_to=upload_location, validators=[validate_size, ])
    meta_description = models.CharField(max_length=160)
    meta_keywords = models.CharField(max_length=160)

    def __str__(self):
        return self.title

    @staticmethod
    def active_first_page():
        return FirstPage.objects.filter(active=True).first() if FirstPage.objects.filter(active=True) else None


class Banner(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to=upload_banner, validators=[validate_size, ], help_text='600*600')
    href = models.URLField(blank=True, null=True)
    new_window = models.BooleanField(default=False)
    big_banner = models.BooleanField(default=False)
    text = HTMLField(blank=True, null=True)

    class Meta:
        ordering = ['active']

    def save(self, *args, **kwargs):
        super(Banner, self).save(*args, **kwargs)
        cache.delete('cache_banners')

    def __str__(self):
        return self.title

    def tag_active(self):
        return 'Active' if self.active else 'No Active'

    def tag_image(self):
        return mark_safe('<img src="%s%s" width="150px" height="150px" class="img-responsive">' %
                         (MEDIA_URL, self.image)) if self.image else None


@receiver(post_save, sender=Brand)
def check_slug_brand(sender, instance, **kwargs):
    if not instance.slug:
        my_slug = slugify(instance.title, allow_unicode=True)
        qs_exists = Brand.objects.filter(slug=my_slug)
        instance.slug = f'{my_slug}-{instance.id}' if qs_exists.exists() else my_slug
        instance.save()