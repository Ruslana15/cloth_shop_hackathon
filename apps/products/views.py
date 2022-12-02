from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as rest_filter
from rest_framework import filters
import django_filters

from .serializers import (
    ProductSerializer,
    ProductListSerializer,
    CategorySerializer,
)
from .models import Product, Category


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    # serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer #/products/
        return ProductSerializer #/product/13/

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    def get_sale(self, price):
        price = int(self.price * (100% - self.sale) / 100)
        return price

    def retrieve(self, request, *args, **kwargs):
        instance: Product = self.get_object() # Product
        instance.views_count += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)

    def get_sale(self):
        instance: Product = self.get_sale()
        instance.price = int(self.price * (100% - self.sale) / 100)
        instance.save()
        return Product

    
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductFilter(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, rest_filter.DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title']
