from datetime import datetime, timedelta
import jwt
from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Role, UserRole
from django.contrib.auth import authenticate
from django.conf import settings
from .context import RegistrationContext, get_registration_strategy

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=200, write_only=True)

    # Shared Field
    date_of_birth = serializers.DateField(
    input_formats=['%d/%m/%Y'],  # Add other formats here if needed
    write_only=True,
    required=False
)

    # Moderator Fields
    id_number = serializers.CharField(write_only=True, required=False)
    address = serializers.CharField(write_only=True, required=False)
    phone_number = serializers.CharField(write_only=True, required=False)

    # Account Holder Fields
    nominee = serializers.CharField(write_only=True, required=False)
    nominee_relationship = serializers.CharField(write_only=True, required=False)
    present_address = serializers.CharField(write_only=True, required=False)
    permanent_address = serializers.CharField(write_only=True, required=False)

    

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'role',
            'date_of_birth',
            'id_number',
            'address',
            'phone_number',
            'nominee',
            'nominee_relationship',
            'present_address',
            'permanent_address',
            
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role_name = validated_data.pop('role', None)

        try:
            role = Role.objects.get(name__iexact=role_name)
        except Role.DoesNotExist:
            raise serializers.ValidationError({'role': 'Role does not exist.'})

        # Create User
        validated_data['username'] = validated_data['username'].lower()
        user = User.objects.create_user(
            
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.is_active =  False
        user.save()

        # Link Role to User
        UserRole.objects.create(user=user, role=role)

        # Run the Strategy to create the role-specific profile
        try:
            strategy = get_registration_strategy(role.name)     
            context = RegistrationContext(strategy)
            context.execute_strategy(user, validated_data)
        except Exception as e:
            user.delete()  # rollback
            raise serializers.ValidationError({'error': str(e)})

        return user

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'username': instance.username,
            'email': instance.email,
            'message': 'User registered successfully'
        }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError('Both username and password are required.')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'Invalid credentials'})

        if not user.check_password(password):
            raise serializers.ValidationError({'detail': 'Invalid credentials'})

        if not user.is_active:
            raise serializers.ValidationError({'detail': 'Account is inactive. Please contact support.'})

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({'detail': 'Authentication failed'})

        payload = {
            'id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow()
        }

        secret_key = getattr(settings, 'SECRET_KEY', 'secret')  # Replace with secure key handling
        token = jwt.encode(payload, secret_key, algorithm='HS256')

        return {
        'username': user.username,  
        'token': token
    }
