# Generated by Django 4.2 on 2023-05-07 15:30

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0045_remove_order_total_order_transaction_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billingaddress',
            old_name='address_line_1',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='billingaddress',
            old_name='address_line_2',
            new_name='company_name',
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='first_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='last_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='phone_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 7, 11, 30, 26, 803687)),
        ),
    ]
