from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='other')

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",  # Prevents conflict with auth.User
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",  # Prevents conflict with auth.User
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
