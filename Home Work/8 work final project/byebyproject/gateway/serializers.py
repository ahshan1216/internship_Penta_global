import random
from rest_framework import serializers
from django.contrib.auth.models import User
from gateway.models import Role, AssignRole, Marchant, Client, Transaction
from django.db import transaction



class ClientRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    pin = serializers.CharField(write_only=True)

    class Meta:
        model = Client
        fields = ['username', 'email', 'password', 'phone_number', 'pin']
    def validate_pin(self, value):
        if not (value.isdigit() and len(value) == 4):
            raise serializers.ValidationError("PIN must be exactly 4 digits and must be numeric.")
        return value
    def create(self, validated_data):
        with transaction.atomic():
          
            if User.objects.filter(username=validated_data['username']).exists():
                raise serializers.ValidationError("Username already exists.")
            
            if User.objects.filter(email=validated_data['email']).exists():
                raise serializers.ValidationError("Email already exists.")
           
            if Client.objects.filter(phone_number=validated_data['phone_number']).exists():
                raise serializers.ValidationError("Phone number already exists.")
       
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
       
        role, _ = Role.objects.get_or_create(name='client')
        AssignRole.objects.create(user=user, role=role)

        
        client = Client.objects.create(
            user=user,
            phone_number=validated_data['phone_number'],
            pin=validated_data['pin']
        )
        return client


class MarchantRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    auth_key = serializers.CharField(read_only=True)
    sec_key = serializers.CharField(read_only=True)

    class Meta:
        model = Marchant
        fields = ['username', 'email', 'password', 'phone_number', 'auth_key', 'sec_key']
        
    def generate_unique_auth_key(self):
        while True:
            key = str(random.randint(10000, 99999))  # 5-digit number
            if not Marchant.objects.filter(auth_key=key).exists():
                return key

    def create(self, validated_data):
       
        with transaction.atomic():
          
            if User.objects.filter(username=validated_data['username']).exists():
                raise serializers.ValidationError("Username already exists.")
           
            if User.objects.filter(email=validated_data['email']).exists():
                raise serializers.ValidationError("Email already exists.")
          
            if Marchant.objects.filter(phone_number=validated_data['phone_number']).exists():
                raise serializers.ValidationError("Phone number already exists.")
            
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
       
        role, _ = Role.objects.get_or_create(name='marchant')
        AssignRole.objects.create(user=user, role=role)
      
        auth_key = self.generate_unique_auth_key()
        sec_key= self.generate_unique_auth_key()
        
        while sec_key == auth_key:
            sec_key = self.generate_unique_auth_key()
        
        marchant = Marchant.objects.create(
            user=user,
            phone_number=validated_data['phone_number'],
            auth_key=auth_key,
            sec_key=sec_key
        )
        return marchant

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['username'] = instance.user.username
        rep['email'] = instance.user.email
       
        return rep
    

class ClintToMarchantPaymentSerializer(serializers.Serializer):
    client_phone = serializers.CharField(max_length=15)
    pin = serializers.CharField(max_length=4)
    merchant_phone = serializers.CharField(max_length=15)
    amount = serializers.IntegerField(min_value=1)

    def validate(self, data):
        client_phone = data['client_phone']
        pin = data['pin']
        merchant_phone = data['merchant_phone']
        amount = data['amount']

        # Validate merchant
        try:
            marchant = Marchant.objects.get(phone_number=merchant_phone)
           
        except Marchant.DoesNotExist:
            raise serializers.ValidationError({"merchant_phone": "Invalid merchant phone number"})
        
        # Validate client
        try:
            client = Client.objects.get(phone_number=client_phone, pin=pin)
        except Client.DoesNotExist:
            raise serializers.ValidationError({"client_phone": "Invalid PIN"})

        # Check balance
        if client.balance < amount:
            Transaction.objects.create(
                user=client.user,
                transaction_type="Pyament_Send",
                amount=amount,
                status="Failed"
            )
            raise serializers.ValidationError({"balance": "Insufficient balance"})

        # Store objects for later use in view
        data['marchant'] = marchant
        data['client'] = client
        return data
    
    
class ClientToClientSendMoneySerializer(serializers.Serializer):
    receiver_phone= serializers.CharField(max_length=15)
    sender_phone=serializers.CharField(max_length=15)
    amount= serializers.IntegerField(min_value=1)
    mypin = serializers.CharField(max_length=4)
    
    def validate(self, data):
        receiver_phone_number=data['receiver_phone']
        sender_phone_number=data['sender_phone']
        amount=data['amount']
        mypin=data['mypin']
        
        try:
            sender_client= Client.objects.get(phone_number=sender_phone_number)
        except:
            raise serializers.ValidationError({"message":"Invalid Sender Phone number"})
        
        try:
            receiver_client= Client.objects.get(phone_number=receiver_phone_number)
        except:
            raise serializers.ValidationError({"message":"Invalid Receiver Phone number"})
        
        # Validate client
        try:
            sender_client_pin = Client.objects.get(phone_number=sender_phone_number,pin=mypin)
        except :
            raise serializers.ValidationError({"My_phone": "Invalid Pin"})
        

        if sender_client_pin.balance < amount :
            Transaction.objects.create(
                user= sender_client_pin.user,
                transaction_type="Send",
                amount=amount,
                status="Failed"
            )
            raise serializers.ValidationError({"balance": "Insufficient balance"})


         # Store objects for later use in view
        data['sender_phone'] = sender_client_pin
        data['receiver_phone'] = receiver_client
        return data
    