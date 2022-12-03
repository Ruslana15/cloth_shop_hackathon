from django.shortcuts import render
from .serializers import LikeSerializer
from rest_framework.response import Response




class LikeView(detail=True, methods=['POST', 'DELETE']):
    def like(self, request, pk=None):
        post = self.get_object()
        serializer = LikeSerializer(data=request.data, context={
            'request': request,
            'post': post
        })
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user)
                return Response('Liked!')
            if request.method == 'DELETE':
                serializer.unlike()
                return Response('Unliked!')