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
                'Thanks for registration Activate your account via linl in your mail',
                status=status.HTTP_201_CREATED
            )

class AccountActivationView(APIView):
    def get(self, request, activation_code):
        user = User.objects.filter(activation_code=activation_code).filter()
        if not user:
            return Response(
                'Page not found',
                status=status.HTTP_404_NOT_FOUND
            )
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response(
            'Account activation ! You can login now',
            status=status.HTTP_200_OK
            )

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request: Response):
        serializers = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.set_new_password()
            return Response(
                'Password succesfull changed',
                status=status.HTTP_200_OK
            )

class RestorePasswordView(APIView):
    def post(self, request: Request):
        serializers = RestorePasswordSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.send_code()
            return Response(
                'Code was sent to your email',
                status=status.HTTP_200_OK
            )

class SetRestorePasswordView(APIView):
    def post(self, request: Response):
        serializers = SetRestoredPasswordSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            return Response(
                "Password re",
                status=status.HTTP_200_OK
            )

class DeleteAccountView(APIView):
    permission_classes = (IsAuthenticated)
    def delete(self, request: Response):
        username = request.username
        User.objects.get(username=username).delete()
        return Response(
            'Account deleted succsesfully',
            status=status.HTTP_204_NO_CONTENT
        )



