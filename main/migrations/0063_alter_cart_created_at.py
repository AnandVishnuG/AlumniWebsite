# Generated by Django 4.2.1 on 2023-05-10 16:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0062_alter_cart_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 10, 12, 32, 58, 25132)),
        ),
    ]
