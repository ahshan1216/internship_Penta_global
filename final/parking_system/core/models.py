from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom user manager
class User(AbstractUser):  
    username = models.CharField(max_length=150, unique=False, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=False)
    email = models.EmailField(max_length=254, unique=True, null=False)
    phone = models.CharField(max_length=11, unique=True, null=False)
    password = models.CharField(max_length=128, null=False ,blank=False)
    is_active = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone']
    def save(self, *args, **kwargs):
        
            self.username = self.email
            super().save(*args, **kwargs)

    def __str__(self):
        return self.username  

# Role Model
class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Assign Role to User
class Assign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} → {self.role.name}"


# KYC Verification
class KYC(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nidf = models.ImageField(upload_to='kyc/nidf/')
    nidb = models.ImageField(upload_to='kyc/nidb/')
    profile = models.ImageField(upload_to='kyc/profile/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"KYC for {self.user.email}"


# Complaint system
class Complain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complain = models.TextField()
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Complain by {self.user.email}"


# Floor map
class Map(models.Model):
    floor = models.CharField(max_length=20)
    file_name = models.ImageField(upload_to='maps/')

    def __str__(self):
        return f"Floor {self.floor}"


# Parking slot
class Parking(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved')
    ]
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    numberplate = models.CharField(max_length=20)
    position = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Slot {self.position} on {self.map.floor} - {self.status}"
