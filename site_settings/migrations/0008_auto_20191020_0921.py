# Generated by Django 2.2 on 2019-10-20 06:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0007_auto_20190605_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentorders',
            name='date_expired',
            field=models.DateField(default=datetime.datetime(2019, 10, 20, 6, 21, 42, 280095, tzinfo=utc)),
        ),
    ]
