# Generated by Django 3.2.5 on 2022-12-03 18:09

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_remove_product_board'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color1',
        ),
        migrations.RemoveField(
            model_name='product',
            name='color2',
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None),
        ),
    ]
