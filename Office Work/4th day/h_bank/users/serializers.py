from rest_framework import serializers
from users.models import Role,UserRole
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email']
        
class RegisterSerializer(serializers.ModelSerializer):
    role=serializers.CharField(max_length=200,write_only=True)
    class Meta:
        model=User
        fields=['username','email','password','role']
        extra_kwargs={'password':{'write_only':True}}
        
    def create(self,validated_data):
        role_name=validated_data.pop('role',None)

        
        if role_name:
            try:

                role=Role.objects.get(name=role_name)
                
            except Role.DoesNotExist:
                raise serializers.ValidationError('Role does not exist')
            
        user=User.objects.create_user(
                validated_data['username'],
                validated_data['email'],
                validated_data['password'])
        
        if role_name:
            UserRole.objects.create(user=user, role=role)
        
        return user

class LoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True,write_only=True)  
    
    class Meta:
        model=User
        fields=['username','password']
    
    
         