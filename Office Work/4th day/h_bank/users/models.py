from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"


#  BaseProfile with common fields
class BaseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()

    class Meta:
        abstract = True

class ModeratorProfile(BaseProfile):
    id_number = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Moderator: {self.user.username}"

class AccountHolderProfile(BaseProfile):
    nominee = models.CharField(max_length=100)
    present_address = models.TextField()
    permanent_address = models.TextField()
    account_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Account Holder: {self.user.username}"
