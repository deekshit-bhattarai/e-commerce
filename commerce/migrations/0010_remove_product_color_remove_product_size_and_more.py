# Generated by Django 5.2 on 2025-05-16 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0009_alter_order_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='od_6f2cf944', primary_key=True, serialize=False, unique=True),
        ),
    ]
