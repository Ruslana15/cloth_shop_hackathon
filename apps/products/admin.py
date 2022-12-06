from django.contrib import admin
from .models import Category, Product, ProductImage


class TabularInlineImage(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['image']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
     list_display = (
        'title',
        'category',
        'price',
        'quantity',
        'slug',
        'in_stock',
        'created_at' 
        )
     inlines = [TabularInlineImage, ]
     list_filter = (
          'title',
          'category',
          'price',
          'quantity',
          'slug',
          'in_stock',
          'created_at')
     search_fields = ('title',)
     # readonly_fields = ('views_count',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
     list_display = ('title', 'parent_category')
     list_filter = ('title', 'parent_category')


