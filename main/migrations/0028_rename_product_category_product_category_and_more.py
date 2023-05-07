# Generated by Django 4.2 on 2023-05-06 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_poll_rename_products_product_alter_post_category_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_category',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='product_desc',
            new_name='desc',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='product_image',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='product_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='product_price',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='product_subcategory',
            new_name='subcategory',
        ),
    ]