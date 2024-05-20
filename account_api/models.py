from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

class UserManager(BaseUserManager):
    def create_user(self, first_name: str, last_name: str, email: str, password: str, is_staff=False, is_superuser=False):
        if not email:
            raise ValueError("User must have an email")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, is_staff=is_staff, is_superuser=is_superuser)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, first_name: str, last_name: str, email: str, password: str):
        return self.create_user(first_name=first_name, last_name=last_name, email=email, password=password, is_staff=True, is_superuser=True)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(verbose_name="First Name", max_length=255)
    last_name = models.CharField(verbose_name="Last Name", max_length=255)
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

