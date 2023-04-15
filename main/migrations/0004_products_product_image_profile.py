# Generated by Django 4.2 on 2023-04-05 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_image',
            field=models.ImageField(default='', upload_to='shop/images'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('desc', models.TextField(max_length=500)),
                ('phonenumber', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.users')),
            ],
        ),
    ]