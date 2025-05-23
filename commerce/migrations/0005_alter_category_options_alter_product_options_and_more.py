# Generated by Django 5.2 on 2025-05-16 08:20

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0004_alter_order_order_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-name'], 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.FloatField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='on_discount',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='od_6ad47086', primary_key=True, serialize=False, unique=True),
        ),
    ]
