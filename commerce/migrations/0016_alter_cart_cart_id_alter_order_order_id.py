# Generated by Django 5.2 on 2025-05-19 04:19

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0015_alter_cart_id_alter_order_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.UUIDField(default=uuid.uuid4, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='od_680ee360', primary_key=True, serialize=False, unique=True),
        ),
    ]
