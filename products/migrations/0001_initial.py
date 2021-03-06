# Generated by Django 2.0.5 on 2019-02-15 06:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import products.tools
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('frontend', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Characteristics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('costum_ordering', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=120, unique=True)),
                ('user_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CharacteristicsValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('costum_ordering', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=120, unique=True)),
                ('user_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=150)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('costum_ordering', models.IntegerField(default=1)),
                ('code_id', models.CharField(blank=True, max_length=25, verbose_name='Κωδικός Χρώματος')),
                ('user_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '5. Χρώματα',
                'ordering': ['-costum_ordering'],
            },
        ),
        migrations.CreateModel(
            name='Gifts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('gift_message', models.CharField(max_length=200, unique=True)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=150)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('costum_ordering', models.IntegerField(default=1)),
                ('site_active', models.BooleanField(default=True, verbose_name='Εμφανίζετε στο Site')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Εμφανίζετε στην πρώτη σελίδα')),
                ('size', models.BooleanField(default=False, verbose_name='Μεγεθολόγιο')),
                ('qty_kilo', models.DecimalField(decimal_places=3, default=1, max_digits=5, verbose_name='Βάρος/Τεμάχια ανά Συσκευασί')),
                ('qty', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Qty')),
                ('barcode', models.CharField(blank=True, max_length=6, null=True, verbose_name='Κωδικός/Barcode')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Περιγραφή')),
                ('measure_unit', models.CharField(blank=True, choices=[('1', 'Τεμάχια'), ('2', 'Κιλά'), ('3', 'Κιβώτια')], default='1', max_length=1, null=True)),
                ('safe_stock', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('sku', models.CharField(blank=True, max_length=150, null=True)),
                ('site_text', tinymce.models.HTMLField(blank=True, null=True)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Price')),
                ('price_b2b', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Τιμή Χονδρικής')),
                ('price_discount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Discount Price.')),
                ('final_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontend.Brand', verbose_name='Brand Name')),
                ('category_site', models.ManyToManyField(blank=True, null=True, related_name='products', to='frontend.CategorySite')),
            ],
            options={
                'verbose_name_plural': '1. Products',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ProductCharacteristics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Characteristics')),
                ('value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.CharacteristicsValue')),
            ],
        ),
        migrations.CreateModel(
            name='ProductPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='600*600', upload_to=products.tools.product_directory_path, validators=[django.core.validators.FileExtensionValidator(['jpg', 'png']), products.tools.check_size])),
                ('alt', models.CharField(blank=True, help_text='Θα δημιουργηθεί αυτόματα εάν δεν συμπληρωθεί', max_length=200, null=True)),
                ('title', models.CharField(blank=True, help_text='Θα δημιουργηθεί αυτόματα εάν δεν συμπληρωθεί', max_length=100, null=True)),
                ('active', models.BooleanField(default=True)),
                ('is_primary', models.BooleanField(default=False, verbose_name='Αρχική Εικόνα')),
                ('is_back', models.BooleanField(default=False, verbose_name='Δεύτερη Εικόνα')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.Product')),
            ],
            options={
                'verbose_name_plural': 'Gallery',
                'ordering': ['is_primary'],
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=150)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('costum_ordering', models.IntegerField(default=1)),
                ('user_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '6. Μεγέθη',
                'ordering': ['costum_ordering'],
            },
        ),
        migrations.CreateModel(
            name='SizeAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Ποσότητα')),
                ('product_related', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_sizes', to='products.Product', verbose_name='Προϊόν')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='products.Size', verbose_name='Νούμερο')),
            ],
            options={
                'verbose_name_plural': '2. Μεγεθολόγιο',
                'ordering': ['title'],
            },
            managers=[
                ('my_query', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='characteristics',
            field=models.ManyToManyField(to='products.ProductCharacteristics'),
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Color', verbose_name='Color'),
        ),
        migrations.AddField(
            model_name='product',
            name='different_color',
            field=models.ManyToManyField(blank=True, related_name='_product_different_color_+', to='products.Product'),
        ),
        migrations.AddField(
            model_name='product',
            name='related_products',
            field=models.ManyToManyField(blank=True, related_name='_product_related_products_+', to='products.Product'),
        ),
        migrations.AddField(
            model_name='product',
            name='user_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Vendor'),
        ),
        migrations.AddField(
            model_name='gifts',
            name='product_related',
            field=models.ManyToManyField(related_name='product_related', to='products.Product'),
        ),
        migrations.AddField(
            model_name='gifts',
            name='products_gift',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='sizeattribute',
            unique_together={('title', 'product_related')},
        ),
    ]
