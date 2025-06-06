# Generated by Django 5.2 on 2025-05-28 04:48

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0002_initial'),
        ('order', '0004_remove_orderhistory_completed_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderhistory',
            name='completed_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='commerce.userprofile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='od_eb9e6519', primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.UUIDField(default=uuid.UUID('d1fbbb7c-bbf7-40f3-be6b-a654b00ddd68')),
        ),
    ]
