# Generated by Django 4.2 on 2023-04-10 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_rename_date_modified_profile_last_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='full_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.IntegerField(blank=True, max_length=10, null=True),
        ),
    ]
