from django.shortcuts import render
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

# Create your views here.
class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginUserAPIView(APIView):
    def post(self, request):
        identifier = request.data.get("identifier")  # can be email or phone
        password = request.data.get("password")
        print(identifier)
        if not identifier or not password:
            return Response({"detail": "Identifier and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Try email first
        print(identifier)
        user = User.objects.filter(email=identifier).first()
        if not user:
            # Try phone if not found by email
            user = User.objects.filter(phone=identifier).first()

        if user and user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.id,
                "email": user.email,
                "name": user.first_name,
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)