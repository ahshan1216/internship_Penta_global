from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,LoginSerializer
# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User create Successfully", "details":serializer.data },status=status.HTTP_201_CREATED)
        return Response({"message":"Failed", "details":serializer.data },status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message":"Login Successfully", "details":serializer.data },status=status.HTTP_200_OK)
        return Response({"message":"Failed", "details":serializer.data },status=status.HTTP_400_BAD_REQUEST)