# accounts/serializers.py
from rest_framework import serializers
from .models import User, AccountHolder, Moderator

class AccountHolderRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    dob = serializers.DateField()
    nominee = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ModeratorRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    dob = serializers.DateField()
    nominee = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class DepositSerializer(serializers.Serializer):
    account_number = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

class TransferSerializer(serializers.Serializer):
    sender_account = serializers.CharField()
    receiver_account = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    transaction_method = serializers.ChoiceField(choices=['bank_transfer', 'paypal_transfer', 'wire_transfer'])
