from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters import rest_framework as rest_filter
from rest_framework import filters
import django_filters
from .permissions import IsOwner, IsStaff
from rest_framework.decorators import action

from .serializers import (
    ProductSerializer,
    ProductListSerializer,
    CategorySerializer,
    HomepageSerializer,
    ProductCreateSerializer,
    ProductSerializerTop
)
from .models import Product, Category, ProductImage


from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    # serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create_product(self):
        if self.action == 'create':
            return ProductCreateSerializer
        return super().get_serializer_class()

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
    # filter_backends = [filters.SearchFilter, rest_filter.DjangoFilterBackend, filters.OrderingFilter]
    # search_fields = ['title',]


class ProductFilter(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, rest_filter.DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'price']
    

class HomepageViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = HomepageSerializer
    filter_backends = [filters.SearchFilter, rest_filter.DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'user__username']
    # filterset_fields = ['tag']
    ordering_fields = ['created_at']
    
    @method_decorator(cache_page(60*60*2))
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return HomepageSerializer
        elif self.action == 'create':
            return ProductCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [IsAdminUser]

        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action == 'comment' and self.request.method == 'DELETE':
            self.permission_classes = [IsOwner]
        if self.action in ['comment']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        if self.action in ['product']:
            self.permission_classes = [IsStaff]
        return super().get_permissions()

    # def retrieve(self, request, *args, **kwargs):
    #     instance: Article = self.get_object.order_by('-views_count').values() # Homepage
    #     instance.views_count += 1
    #     instance.save()
    #     return super().retrieve(request, *args, **kwargs)

    @action(methods=["GET"], detail=False, url_path="")
    def first_ten_top(self, request):
        products = Product.objects.order_by('-views_count').values()
        # print(products)
        serializer = ProductSerializerTop(products, many=True).data[:10]
        return Response(data=serializer)

