# Generated by Django 4.2 on 2023-05-06 02:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_cart_cartitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 5, 22, 56, 31, 654016)),
        ),
        migrations.AddField(
            model_name='cart',
            name='isPaid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cart',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]