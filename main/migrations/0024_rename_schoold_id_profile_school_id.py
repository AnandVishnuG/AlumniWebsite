# Generated by Django 4.2 on 2023-05-01 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_profile_schoold_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='schoold_id',
            new_name='school_id',
        ),
    ]
