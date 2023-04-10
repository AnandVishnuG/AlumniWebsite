# Generated by Django 4.2 on 2023-04-03 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_user_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_category', models.CharField(default='', max_length=100)),
                ('product_subcategory', models.CharField(default='', max_length=50)),
                ('product_price', models.IntegerField()),
                ('product_desc', models.CharField(max_length=300)),
            ],
        ),
    ]
