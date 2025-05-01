from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,LoginSerializer,BankTransferSerializer
import jwt
from django.contrib.auth.models import User
from .models import AccountHolderProfile , Transaction
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
            roles = [user_role.role.name for user_role in user.user_roles.all()] or ['No Role Selected'] #not clear
            roles_string = ", ".join(roles)
            
            account=AccountHolderProfile.objects.get(user=user)

            return Response({
                "message": f"Welcome to H_Bank PLC" ,
                "roles": roles_string,
                "username": user.username,
                "balance": str(account.balance),
                "account_number": account.account_number
                
            })
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            return Response({"message": "Token has expired."}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"message": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

# views.py
class BankTransferView(APIView):
    def post(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            return Response({"message": "Authentication required."}, status=401)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['id'])

            if not user.is_active:
                return Response({"message": "User account is inactive."}, status=403)

            try:
                sender_account = AccountHolderProfile.objects.get(user=user)
            except AccountHolderProfile.DoesNotExist:
                return Response({"message": "Sender has no account."}, status=403)

            serializer = BankTransferSerializer(data=request.data)
            if serializer.is_valid():
                receiver_account = serializer.validated_data["receiver_account"]
                amount = serializer.validated_data["balance"]

                if sender_account.balance < amount:
                    return Response({"message": "Insufficient funds."}, status=400)

                # Transfer funds
                sender_account.balance -= amount
                receiver_account.balance += amount

                sender_account.save()
                receiver_account.save()

                Transaction.objects.create(
                    account_holder=sender_account,
                    transaction_type='debit',
                    amount=amount
                )
                
                Transaction.objects.create(
                    account_holder=receiver_account,
                    transaction_type='credit',
                    amount=amount
                )

                return Response({
                    "message": f"Transferred {amount} to {receiver_account.account_number}",
                    "sender_balance": str(sender_account.balance)
                }, status=200)

            return Response({"errors": serializer.errors}, status=400)

        except jwt.ExpiredSignatureError:
            return Response({"message": "Token expired."}, status=401)
        except jwt.InvalidTokenError:
            return Response({"message": "Invalid token."}, status=401)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=404)

class TransactionHistoryView(APIView):
    def get(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            return Response({"message": "Authentication required."}, status=401)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['id'])

            if not user.is_active:
                return Response({"message": "User account is inactive."}, status=403)

            try:
                account = AccountHolderProfile.objects.get(user=user)
                transactions = Transaction.objects.filter(account_holder=account).order_by('-date')
                transaction_list = [
                    {
                        "transaction_type": transaction.transaction_type,
                        "amount": str(transaction.amount),
                        "date": transaction.date.strftime("%d-%m-%Y %H:%M:%S")
                    } for transaction in transactions
                ]

                return Response({
                    "transactions": transaction_list
                }, status=200)

            except AccountHolderProfile.DoesNotExist:
                return Response({"message": "Account not found."}, status=404)

        except jwt.ExpiredSignatureError:
            return Response({"message": "Token expired."}, status=401)
        except jwt.InvalidTokenError:
            return Response({"message": "Invalid token."}, status=401)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=404)   
    
    
    
class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        return response