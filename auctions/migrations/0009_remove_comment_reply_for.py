# Generated by Django 4.1 on 2023-07-07 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_comment_reply_for'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='reply_for',
        ),
    ]
