from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('STAFF', 'Staff'),
        ('ADMIN', 'System Admin'),
        ('SUPPORT', 'IT Support'),
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username
