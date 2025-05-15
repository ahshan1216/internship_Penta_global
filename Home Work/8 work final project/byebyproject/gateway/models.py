from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Role(models.Model):
    name=models.CharField(max_length=50,unique=True)
    
    def __str__(self):
        return self.name

class AssignRole(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    role=models.ForeignKey(Role,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

    
class Marchant(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_key=models.CharField(max_length=255,unique=True)
    sec_key=models.CharField(max_length=255)
    phone_number=models.CharField(max_length=15,unique=True)
    balance= models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.user.username
    
class Client(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=15,unique=True)
    balance= models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    pin = models.CharField(max_length=4, null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Send', 'Send'),
        ('Receive', 'Receive'),
        ('Withdraw', 'Withdraw'),
        ('Deposit', 'Deposit'),
        ('Pyament_Send', 'Payment_Send'),
        ('Payment_Receive', 'Payment_Receive'),  #1st er ta database value 2nd ta database view
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    transaction_type=models.CharField(max_length=20,choices=TRANSACTION_TYPES)
    amount=models.DecimalField(max_digits=12, decimal_places=2)
    date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=10,default='Pending',choices=STATUS_CHOICES)
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount} - {self.status} "
    
class Agent(Client):
    pass

    