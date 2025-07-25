from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ClientRegisterSerializer,
    MarchantRegisterSerializer,
    ClientToClientSendMoneySerializer
)
from .serializers import ClintToMarchantPaymentSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import AssignRole , Marchant ,Transaction
from .jwtpayload import create_jwt_token
import jwt
from django.conf import settings
from django.db import transaction

class AuthTypeView(APIView):
    def get(self, request):
        return Response({
            "register": {
                "client": "/api/register/client/",
                "marchant": "/api/register/marchant/"
            },
            "login": {
                "client": "/api/login/client/",
                "marchant": "/api/login/marchant/"
            }
        })


class ClientRegisterView(APIView):
    def post(self, request):
        serializer = ClientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            marchant=serializer.save()
            respose=MarchantRegisterSerializer(marchant).data
            return Response({"details": respose}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarchantRegisterView(APIView):
    def post(self, request):
        serializer = MarchantRegisterSerializer(data=request.data)
        if serializer.is_valid():
            marchant=serializer.save()
            print(marchant)
            respose=MarchantRegisterSerializer(marchant).data
            print(respose)
            return Response({"message": respose}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            if AssignRole.objects.filter(user=user, role__name="client").exists():
                token = create_jwt_token(user)
                response= Response({"message": "login Successful"})
                response.set_cookie(
                    key="access_token",
                    value=token,
                    httponly=True,  # Prevent access via JavaScript
                    secure=False,   # Set to True in production with HTTPS
                    
                )
                return response
            return Response({"error": "Not a client user"}, status=403)
        return Response({"error": "Invalid credentials"}, status=401)


class MarchantLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)


        if user:
            if AssignRole.objects.filter(user=user, role__name="marchant").exists():
                token = create_jwt_token(user)
                response= Response({"message": "login Successful"})
                response.set_cookie(
                    key="access_token",
                    value=token,
                    httponly=True,  # Prevent access via JavaScript
                    secure=False,   # Set to True in production with HTTPS
                    
                )
                return response
            return Response({"error": "Not a Marchant user"}, status=403)
        return Response({"error": "Invalid credentials"}, status=401)
    
    
class MarchantDashboardView(APIView):
    def get(self, request):
        Token = request.COOKIES.get("access_token")
        if not Token:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            payload = jwt.decode(Token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            user = User.objects.get(id=payload["user_id"])

            if not AssignRole.objects.filter(user=user, role__name="marchant").exists():
                return Response({"error": "Not a Marchant user"}, status=status.HTTP_403_FORBIDDEN)
            marchant_data = {
                "message": "Welcome to the Marchant Dashboard",
                "user": user.username,
                "email": user.email,
                "phone_number": user.marchant.phone_number,
                "balance": user.marchant.balance,
                "auth_key": user.marchant.auth_key,
                "sec_key": user.marchant.sec_key,
           
        }
            return Response(marchant_data, status=status.HTTP_200_OK)
        
        except:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            
        
class ClintToMarchantPayment(APIView):
    def post(self, request, phone_number, amount):


            # Combine URL data into request data
            request_data = {
                "merchant_phone": phone_number,
                "amount": amount,
                **request.data  # Include additional data from the request body
            }
            
            serializer = ClintToMarchantPaymentSerializer(data=request_data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)

            client = serializer.validated_data['client']
            marchant = serializer.validated_data['marchant']

            with transaction.atomic():
                client.balance -= amount
                marchant.balance += amount
                client.save()
                marchant.save()

                Transaction.objects.create(
                    user=client.user,
                    transaction_type="Payment_Send",
                    amount=amount,
                    status="Completed"
                )
                Transaction.objects.create(
                    user=marchant.user,
                    transaction_type="Payment_Receive",
                    amount=amount,
                    status="Completed"
                )

            return Response({
                "message": f"Payment of {amount} Taka successful",
                "from": client.user.username,
                "to": marchant.user.username,
            }, status=200)
        


class ClintToClientSendMoney(APIView):
    def post(self, request, sender_phone, amount):
        token = request.COOKIES.get("access_token")
        if not token:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            user = User.objects.get(id=payload["user_id"])

            if not AssignRole.objects.filter(user=user, role__name="client").exists():
                return Response({"error": "Not a client user"}, status=status.HTTP_403_FORBIDDEN)

            if user.client.phone_number != sender_phone:
                return Response({"error": "Unauthorized: Phone number mismatch"}, status=status.HTTP_403_FORBIDDEN)

            request_data = {
                "sender_phone": sender_phone,
                "amount": amount,
                **request.data  
            }

            serializer = ClientToClientSendMoneySerializer(data=request_data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)

            sender = serializer.validated_data['sender_phone']
            receiver = serializer.validated_data['receiver_phone']

            with transaction.atomic():
                sender.balance -= amount
                receiver.balance += amount

                sender.save()
                receiver.save()

                Transaction.objects.create(
                    user=sender.user,
                    transaction_type="Send",
                    amount=amount,
                    status="Completed"
                )
                Transaction.objects.create(
                    user=receiver.user,
                    transaction_type="Receive",
                    amount=amount,
                    status="Completed"
                )

            return Response({"message": "Client to Client payment successful"}, status=status.HTTP_200_OK)
#https://pyjwt.readthedocs.io/en/stable/api.html aikhan theke powa
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


   
    
class MarchantTransactionHistoryView(APIView):
    def get(self, request):
        Token = request.COOKIES.get("access_token")
        if not Token:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            payload = jwt.decode(Token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            user = User.objects.get(id=payload["user_id"])
            print(user)
            if not AssignRole.objects.filter(user=user, role__name="marchant").exists():
                return Response({"error": "Not a Marchant user"}, status=status.HTTP_403_FORBIDDEN)
            
            transactions = user.transaction_set.all()
            transaction_data = [
                {
                    "transaction_type": transaction.transaction_type,
                    "amount": transaction.amount,
                    "date": transaction.date,
                    "status": transaction.status
                }
                for transaction in transactions
                    
            ]
            return Response(transaction_data, status=status.HTTP_200_OK)
        
        except:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

class Agent(APIView):
    pass
          
class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out successfully"})
        response.delete_cookie("access_token")
        return response