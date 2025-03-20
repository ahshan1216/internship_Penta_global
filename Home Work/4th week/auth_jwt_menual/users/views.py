from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework.exceptions import AuthenticationFailed
import jwt
from datetime import datetime, timedelta
# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = CustomUser.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload,'secret',algorithm='HS256')
        
        response= Response()
        
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data={
            'jwt': token
            
            }
        
        return response
    
    
    
    
class UserView(APIView):
        def get(self, request):
            token = request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed('Unauthenticated')
            
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated')
            
            user = CustomUser.objects.filter(id=payload['id']).first()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout success'
        }
        return response