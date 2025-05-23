# Generated by Django 5.2 on 2025-05-16 11:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commerce", "0007_remove_product_color_remove_product_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="color",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="commerce.productcolor",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="size",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="commerce.productsize",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="order",
            name="order_id",
            field=models.CharField(
                default="od_daff2394", primary_key=True, serialize=False, unique=True
            ),
        ),
    ]
