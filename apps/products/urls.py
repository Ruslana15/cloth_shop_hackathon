from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, ProductFilter, HomepageViewSet


router = DefaultRouter()
router.register('products', ProductViewSet, 'product')
router.register('categories', CategoryViewSet, 'category')
router.register('product_filter', ProductFilter, 'search')
router.register('homepage', HomepageViewSet, 'homepage')

urlpatterns = [
    path('', include('apps.review.urls')),
    
]
urlpatterns += router.urls