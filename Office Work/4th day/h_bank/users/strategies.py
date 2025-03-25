from abc import ABC, abstractmethod
import random
from users.models import ModeratorProfile, AccountHolderProfile

# Base Strategy Interface
class RegistrationStrategy():



    #  Shared method to get DOB
    def get_date_of_birth(self, validated_data):
        dob = validated_data.get('date_of_birth')
        if not dob:
            raise ValueError('date_of_birth is required.')
        return dob


# Moderator Strategy
class ModeratorRegistrationStrategy(RegistrationStrategy):

    def register_profile(self, user, validated_data):
        date_of_birth = self.get_date_of_birth(validated_data)

        required_fields = ['id_number', 'address', 'phone_number']
        for field in required_fields:
            if not validated_data.get(field):
                raise ValueError(f'{field} is required for moderator registration.')

        ModeratorProfile.objects.create(
            user=user,
            id_number=validated_data['id_number'],
            address=validated_data['address'],
            phone_number=validated_data['phone_number'],
            date_of_birth=date_of_birth
        )


# Account Holder Strategy
class AccountHolderRegistrationStrategy(RegistrationStrategy):

    def register_profile(self, user, validated_data):
        date_of_birth = self.get_date_of_birth(validated_data)

        required_fields = ['nominee', 'present_address', 'permanent_address']
        for field in required_fields:
            if not validated_data.get(field):
                raise ValueError(f'{field} is required for account holder registration.')

# Generate a random unique 13-digit account number if it's not provided
        if 'account_number' not in validated_data or not validated_data['account_number']:
            validated_data['account_number'] = self.generate_unique_account_number()
            
        AccountHolderProfile.objects.create(
            user=user,
            nominee=validated_data['nominee'],
            present_address=validated_data['present_address'],
            permanent_address=validated_data['permanent_address'],
            account_number=validated_data['account_number'],
            date_of_birth=date_of_birth
        )
        
        
    def generate_unique_account_number(self):
            """Generate a random unique 13-digit account number."""
            while True:
                account_number = str(random.randint(1000000000000, 9999999999999))  # 13-digit number
                # Check if account number already exists in the database
                if not AccountHolderProfile.objects.filter(account_number=account_number).exists():
                    return account_number