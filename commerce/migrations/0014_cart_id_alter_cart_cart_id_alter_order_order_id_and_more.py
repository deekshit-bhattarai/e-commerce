# Generated by Django 5.2 on 2025-05-19 03:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0013_alter_order_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.UUIDField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='od_3f6188dd', primary_key=True, serialize=False, unique=True),
        ),
        migrations.CreateModel(
            name='UserComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=600)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commerce.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='commerce.usercomments'),
        ),
        migrations.CreateModel(
            name='UserReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.CharField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], max_length=10)),
                ('review_comment', models.CharField(max_length=600)),
                ('review_created_at', models.DateTimeField(auto_now_add=True)),
                ('review_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commerce.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='review',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='commerce.userreview'),
        ),
    ]
