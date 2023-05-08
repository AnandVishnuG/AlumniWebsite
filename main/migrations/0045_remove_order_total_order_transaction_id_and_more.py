# Generated by Django 4.2 on 2023-05-07 14:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0044_remove_order_isshippable_alter_cart_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total',
        ),
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_isDigital',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 7, 10, 55, 32, 431000)),
        ),
    ]