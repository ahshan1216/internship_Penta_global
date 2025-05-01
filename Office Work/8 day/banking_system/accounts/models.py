from django.db import models 
from django.contrib.auth.models import AbstractUser , Group

# Create your models here.
class User(AbstractUser):
    # Extend the default User model if needed
    pass

class AccountHolder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    dob = models.DateField()
    nominee = models.CharField(max_length=255)
    account_number = models.CharField(max_length=5, unique=True, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        # Generate account number if it's not already set
        if not self.account_number:
            # Get the last account number and increment it
            last = AccountHolder.objects.order_by('-account_number').first()
            if last and last.account_number and last.account_number.isdigit():
                new_num = int(last.account_number) + 1
            else:
                new_num = 10001  # Starting account number
            self.account_number = str(new_num).zfill(5)  # Ensure it's 5 digits (e.g., 10001)

        super().save(*args, **kwargs)  # Save the object with the generated account number

    def __str__(self):
        return f"{self.full_name} ({self.account_number})"

class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    dob = models.DateField()
    nominee = models.CharField(max_length=255)
    
class Transaction(models.Model):
    sender = models.ForeignKey(AccountHolder, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(AccountHolder, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)