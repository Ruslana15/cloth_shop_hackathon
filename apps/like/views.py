from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LikeSerializer
from rest_framework.response import Response



class LikeView(APIView):
    serializers_class = LikeSerializer

    def post(self, request, pk=None):
        # product = self.get_object()
        serializer = LikeSerializer(data=request.data, context={
            'request': request,
            # 'product': product
        })
        if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response('Liked!')

    def delete(self, request):
        serializer = LikeSerializer(data=request.data, context={
            'request': request,
            # 'product': product
        })
        if serializer.is_valid(raise_exception=True):
                serializer.unlike()
                return Response('Unliked!')
