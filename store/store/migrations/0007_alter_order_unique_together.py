# Generated by Django 4.2.4 on 2023-09-01 23:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0006_orderitem_order_item"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="order",
            unique_together=set(),
        ),
    ]
