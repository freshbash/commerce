# Generated by Django 4.1 on 2023-07-04 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.FloatField(),
        ),
    ]
