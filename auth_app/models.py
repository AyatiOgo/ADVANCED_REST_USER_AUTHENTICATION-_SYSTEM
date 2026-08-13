from django.db import models
from django.contrib.auth.base_user import  BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import random
# Create your models here.

class UserManager(BaseUserManager):

    def _create_user(self, email, password=None, **extra_fields ):
        if not email:
            raise ValueError('Email Input is Invalid')
        email = self.normalize_email(email)

        first_name = extra_fields.get('fist_name', '')
        last_name = extra_fields.get('last_name', '')

        username = F'{first_name}{last_name}{random.randint(10,99)}'

        while self.model.objects.filter(username__iexact = username).exists():
            username = F'{first_name}{last_name}{random.randint(10,99)}'


        user = self.model(email = email, username = username, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_user(self, email, password=None, **extra_fields ):
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email=email, 
                                 password=password,
                                 **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields ):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)

        return self._create_user(email=email, 
                                 password=password,
                                 **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=150)
    username = models.CharField(unique=True, max_length=150, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD ='email'

    def __str__(self):
        return f'{self.email}'

