from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .serializers import CommentSerializer
from .models import Comment
from apps.products.permissions import IsOwner
from rest_framework import mixins, status
from rest_framework.response import Response


class CreateComment(detail=True, methods=['POST', 'DELETE']):
    def comment(self, request, pk=None):
        product = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, product=product)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
                )


class CommentCreateDeleteView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwner]
