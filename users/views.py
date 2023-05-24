from .serializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):
    """
    User registration API
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
   

class UserLoginView(TokenObtainPairView):
    """User Login APIView"""
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainPairSerializer
