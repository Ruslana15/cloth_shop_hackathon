# Generated by Django 3.2.16 on 2022-11-26 12:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=100, primary_key=True, serialize=False)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='products.category', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=220, primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField(default=0)),
                ('in_stock', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to='product_images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('views_count', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
            ],
        ),
    ]
