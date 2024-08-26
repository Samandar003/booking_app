from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser, Group, PermissionsMixin
from fcm_django.models import FCMDevice
from django.contrib.auth import get_user_model

class CustomUserModel(AbstractUser, PermissionsMixin):
    CITIES=(
        ("Tashkent", "Tashkent"),
        ("Navoiy", "Navoiy"),
        ("Buxoro", "Buxoro"),
        ("Namangan", "Namangan"),
        ("Navoiy", "Navoiy"),
        ("Navoiy", "Navoiy"),
        ("Navoiy", "Navoiy"),
        ("Navoiy", "Navoiy"),
        
        
    )
    username=models.CharField(max_length=200)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    email=models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=15, unique=True)  # Add max_length attribute    card=models.CharField(max_length=20)
    city=models.CharField(max_length=100, choices=CITIES)
    municipality=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects=CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=["first_name", "last_name", "city", "username"]       
  
    
    def __str__(self):
        return self.email
    
class UserDevice(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    device = models.ForeignKey(FCMDevice, on_delete=models.CASCADE)

    def __str__(self):
        return self.user + ' ' + self.device
    