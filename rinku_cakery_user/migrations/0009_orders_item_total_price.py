# Generated by Django 5.0.6 on 2024-07-16 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rinku_cakery_user', '0008_remove_orders_item_message_on_cake_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders_item',
            name='total_price',
            field=models.CharField(default=0, max_length=150),
            preserve_default=False,
        ),
    ]
