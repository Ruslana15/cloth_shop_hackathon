from django.shortcuts import render
from rest_framework.views import APIView

from apps.products.models import Product
from .serializers import LikeSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class LikeView(APIView):
    serializers_class = LikeSerializer
    
    @swagger_auto_schema(request_body=LikeSerializer)
    def post(self, request):
            # product = self.get_object()
            # prod = Product.objects.filter(slug=pk)
            serializer = LikeSerializer(data=request.data, context={
                'request': request,
                # 'product': product
            })
            if serializer.is_valid(raise_exception=True):
                    serializer.created(user=request.user)
                    return Response('Liked!')

    @swagger_auto_schema(request_body=LikeSerializer)
    def delete(self, request):
        serializer = LikeSerializer(data=request.data, context={
                'request': request,
                # 'product': product
            })
        if serializer.is_valid(raise_exception=True):
                serializer.unlike()
                return Response('Unliked!')
