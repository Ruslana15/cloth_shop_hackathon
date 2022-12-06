from rest_framework import routers
from .views import LikeView
from django.urls import path


urlpatterns = [
    path('like/<str:slug>/', LikeView.as_view())
]
