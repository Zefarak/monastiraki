# Generated by Django 2.0.7 on 2019-04-18 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_price_from'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='show_price',
            field=models.BooleanField(default=False, verbose_name='Δείξε Τιμή'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_from',
            field=models.BooleanField(default=False, verbose_name='Τιμή Από'),
        ),
    ]
