# Generated by Django 4.2.1 on 2023-05-10 18:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0066_alter_cart_created_at_alter_poll_publish_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 10, 14, 1, 29, 129737)),
        ),
    ]