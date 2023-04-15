# Generated by Django 4.2 on 2023-04-14 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=20)),
                ('photo', models.ImageField(upload_to='user/images')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='', upload_to='user/avatar'),
        ),
    ]
