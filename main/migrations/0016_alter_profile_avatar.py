# Generated by Django 4.2 on 2023-04-14 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_profile_bio_alter_profile_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='', upload_to='user/avatar'),
        ),
    ]