from rest_framework import routers
from django.urls import path, include

from .views import CommentView


router = routers.DefaultRouter()
router.register('comments', CommentView, 'comment')


urlpatterns = [
    # path('review/', CommentView.as_view(), name='comment')
    # path('shop/', include('apps.review.urls')),


]
urlpatterns += router.urls
