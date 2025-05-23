# Generated by Django 5.2 on 2025-05-20 06:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0023_cart_created_at_cart_session_key_cart_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='commerce.userprofile'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='od_786e9301', primary_key=True, serialize=False, unique=True),
        ),
    ]
