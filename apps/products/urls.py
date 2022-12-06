from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, ProductFilter, HomepageViewSet,CategoryFilter

router = DefaultRouter()
router.register('products', ProductViewSet, 'product')
router.register('categories', CategoryViewSet, 'category')
router.register('homepage', HomepageViewSet, 'homepage')
router.register('product_filter', ProductFilter, 'search')
router.register('category_filter', CategoryFilter, 'search')


urlpatterns = [
    path('', include('apps.review.urls')),
    path('', include('apps.like.urls')),

    
]
urlpatterns += router.urls