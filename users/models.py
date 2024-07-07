from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser, Group
# Create your models here.

class CustomUserModel(AbstractUser):
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
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    email=models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=15, unique=True)  # Add max_length attribute    card=models.CharField(max_length=20)
    city=models.CharField(max_length=100, choices=CITIES)
    municipality=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=["first_name", "last_name", "city"]
    
    objects=CustomUserManager()
    
  
    
    def __str__(self):
        return self.email
    
