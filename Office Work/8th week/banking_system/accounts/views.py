# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, AccountHolder, Moderator, Transaction
from .serializers import *
from django.contrib.auth.models import Group

from .transaction_context import TransactionContext
from .transaction_strategies import BankTransfer, PayPalTransfer, WireTransfer

class RegisterAccountHolder(APIView):
    def post(self, request):
        serializer = AccountHolderRegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = User.objects.create_user(username=data['email'], email=data['email'], password=data['password'])
            acc = AccountHolder.objects.create(user=user, full_name=data['full_name'], dob=data['dob'], nominee=data['nominee'])
            return Response({'msg': 'Account holder registered'}, status=201)
        return Response(serializer.errors, status=400)

class RegisterModerator(APIView):
    def post(self, request):
        serializer = ModeratorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = User.objects.create_user(username=data['email'], email=data['email'], password=data['password'])
            mod = Moderator.objects.create(user=user, full_name=data['full_name'], dob=data['dob'], nominee=data['nominee'])
            return Response({'msg': 'Moderator registered'}, status=201)
        return Response(serializer.errors, status=400)

class DepositView(APIView):
    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            acc = AccountHolder.objects.get(account_number=data['account_number'])
            acc.balance += data['amount']
            acc.save()
            return Response({'msg': 'Deposited'}, status=200)
        return Response(serializer.errors, status=400)

class TransferView(APIView):
    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            sender = AccountHolder.objects.get(account_number=data['sender_account'])
            receiver = AccountHolder.objects.get(account_number=data['receiver_account'])
            method = data['transaction_method']

            # strategy selection
            if method == 'bank_transfer':
                strategy = BankTransfer()
            elif method == 'paypal_transfer':
                strategy = PayPalTransfer()
            else:
                strategy = WireTransfer()

            context = TransactionContext(strategy)
            msg = context.execute(sender, receiver, data['amount'])

            Transaction.objects.create(sender=sender, receiver=receiver, amount=data['amount'])
            return Response({'msg': msg}, status=200)
        return Response(serializer.errors, status=400)
