# Generated by Django 5.0.6 on 2024-07-12 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rinku_cakery_user', '0004_checkout_data_orders_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders_item',
            name='cart',
        ),
    ]
