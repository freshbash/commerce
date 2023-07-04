# Generated by Django 4.1 on 2023-07-04 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_bid_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('ANTIQUES', 'Antiques'), ('AUTOMOBILES', 'Automobiles'), ('BOOKS', 'Books/Textbooks'), ('ELECTRONICS', 'Electronics'), ('FASHION', 'Fashion'), ('TOYS', 'Toys'), ('HOME', 'Home/Kitchen')], default='Not Provided', max_length=64),
        ),
    ]