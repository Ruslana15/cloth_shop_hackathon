from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from .serializers import (UserRegistrationSerializer,
PasswordChangeSerializer,
RestorePasswordSerializer,
SetRestoredPasswordSerializer
)
from apps.account import serializers


User = get_user_model()

class RegistrationView(APIView):
    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request: Request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                'Спасибо за регистрацию Активируйте свой аккаунт через почту',
                status=status.HTTP_201_CREATED
            )

class AccountActivationView(APIView):
    def get(self, request, activation_code):
        # user = User.objects.filter(activation_code=activation_code)
        user = get_object_or_404(User, activation_code=activation_code)
        if not user:
            return Response(
                'Page not found',
                status=status.HTTP_404_NOT_FOUND
            )
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response(
            'Аккаунт активирован! Вы можете логинится',
            status=status.HTTP_200_OK
            )

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request: Response):
        serializers = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.set_new_password()
            return Response(
                'Пароль успешно изменен',
                status=status.HTTP_200_OK
            )

class RestorePasswordView(APIView):
    def post(self, request: Request):
        serializers = RestorePasswordSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.send_code() 
            return Response(
                'Код был выслан на вашу почту',
                status=status.HTTP_200_OK
            )

class SetRestorePasswordView(APIView):
    def post(self, request: Response):
        serializers = SetRestoredPasswordSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):  
            return Response(
                "Пароль изменен",
                status=status.HTTP_200_OK
            )

class DeleteAccountView(APIView):
    permission_classes = (IsAuthenticated)
    def delete(self, request: Response):
        username = request.username
        User.objects.get(username=username).delete()
        return Response(
            'Аккаунт успешно удален',
            status=status.HTTP_204_NO_CONTENT
        )



