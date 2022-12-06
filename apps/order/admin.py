from django.contrib import admin
from .models import Order, OrderItems

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')


admin.site.register(Order)
admin.site.register(OrderItems)


