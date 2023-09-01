# Generated by Django 4.2.4 on 2023-08-31 21:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="user_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.DeleteModel(
            name="Customer",
        ),
    ]
