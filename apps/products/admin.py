from django.contrib import admin
from .models import Category, Product, ProductImage


class TabularInlineImage(admin.TabularInline):
    model = ProductImage
    extra = 0
    fields = ['image']


class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [TabularInlineImage, ]
    list_display = ('title', 'category', 'price', 'quantity', 'in_stock')
    fieldsets = (
        (None, {
            "fields": ("title", "slug"),
        }),
        (None, {
            "fields": ("image",),
        }),
        (None, {
            "fields": (("description",),)
        }),
        (None, {
            "fields": ("category",),
        }),
        (None, {
            "fields": (("color1", "color2"),)
        }),
        (None, {
            "fields": ("size",),
        }),
        (None, {
            "fields": (("price", "sale"),)
        }),
        (None, {
            "fields": ("quantity",),
        }),
        (None, {
            "fields": ("in_stock",),
        }),
    )



admin.site.register(Product, ProductAdmin)
admin.site.register(Category)