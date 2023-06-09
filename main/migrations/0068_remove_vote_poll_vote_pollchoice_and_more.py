# Generated by Django 4.2.1 on 2023-05-10 18:03

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0067_alter_cart_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='poll',
        ),
        migrations.AddField(
            model_name='vote',
            name='pollChoice',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='vote_set', to='main.poll_choice'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 10, 14, 3, 13, 753701)),
        ),
    ]
