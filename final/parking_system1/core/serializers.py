from rest_framework import serializers
from .models import User, Role, Assign, KYC, Complain, Map, Parking

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'status']

# Role Serializer
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

# Assign Role Serializer
class AssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assign
        fields = ['id', 'user', 'role']

# KYC Serializer
class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = ['id', 'user', 'nidf', 'nidb', 'profile', 'status']

# Complain Serializer
class ComplainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complain
        fields = ['id', 'user', 'complain', 'status']

# Map Serializer
class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ['id', 'floor', 'file_name']

# Parking Serializer
class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ['id', 'map', 'user', 'numberplate', 'position', 'status', 'amount', 'time']
