from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,LoginSerializer
import jwt
from django.contrib.auth.models import User
from .models import AccountHolderProfile
# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User create Successfully", "details":serializer.data },status=status.HTTP_201_CREATED)
        return Response({"message":"Failed", "details":serializer.errors },status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            username = serializer.validated_data['username']
            
            response = Response({
                "message": "Login Successfully",
                "user": username
            }, status=status.HTTP_200_OK)
            
             # Set token as a cookie (secure and HTTP-only)
            response.set_cookie(
                key='access_token',
                value=token,
                httponly=True,
                secure=True  
            )
            
            return response
        return Response({"message":"Failed", "details":serializer.errors },status=status.HTTP_400_BAD_REQUEST)
    

class DashboardView(APIView):
    def get(self,request):
        token = request.COOKIES.get('access_token')
        
        if not token:
            return Response({"message":"Token not found"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['id'])

            # Fetch roles for the user
            roles = [user_role.role.name for user_role in user.user_roles.all()] or ['No Role Selected']
            roles_string = ", ".join(roles)
            
            account=AccountHolderProfile.objects.get(user=user)

            return Response({
                "message": f"Welcome to {user.username} of {roles_string}" ,
                "balance": str(account.balance),
                "account_number": account.account_number
                
            })
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            return Response({"message": "Token has expired."}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"message": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
