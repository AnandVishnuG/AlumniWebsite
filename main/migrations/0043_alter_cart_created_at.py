# Generated by Django 4.2 on 2023-05-07 04:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_alter_cart_created_at_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 7, 0, 49, 46, 46169)),
        ),
    ]
