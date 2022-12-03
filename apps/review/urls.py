from rest_framework import routers
# from .views import CommentView
from .views import CommentCreateDeleteView

router = routers.DefaultRouter()
router.register('comment', CommentCreateDeleteView, 'comment')
urlpatterns = [
    
]
urlpatterns += router.urls