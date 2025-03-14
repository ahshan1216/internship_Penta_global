from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import CustomUserSerializer, TokenObtainPairSerializer , TodoSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Todo

class SignupView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TodoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
       
        if request.user.role == 'teacher' or request.user.role == 'student':
           
            todos = Todo.objects.all()
            
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
       
        if request.user.role != 'teacher':
            return Response(
                {"detail": "You do not have permission to create a Todo."},
                status=status.HTTP_403_FORBIDDEN
            )

       
        serializer = TodoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
       
        todo = Todo.objects.get(pk=pk)

        if request.user.role == 'teacher':
             serializer = TodoSerializer(todo, data=request.data, partial=True)
        elif request.user.role == 'student':
            
            allowed_fields = {'is_completed'}
            attempted_fields = set(request.data.keys())

            if not attempted_fields.issubset(allowed_fields):
                return Response(
                        {"detail": "You do not have permission to edit fields you only edit is_completed field."},
                    status=status.HTTP_403_FORBIDDEN
            )
            student_data = {'is_completed': request.data.get('is_completed', todo.is_completed)}
            serializer = TodoSerializer(todo, data=student_data, partial=True)
            
        else:
            return Response(
                {"detail": "You do not have permission to update a Todo."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
             
          
          