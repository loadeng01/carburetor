from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            return ValueError('Email is required!')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.create_activation_code()
        user.create_phone_activation_code()
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_phone_active', True)
        return self._create_user(email, password, **kwargs)

    def create_employee(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_phone_active', True)
        return self._create_user(email, password, **kwargs)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=220)
    phone_number = models.CharField(max_length=25, blank=True, null=True, unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    activation_code = models.CharField(max_length=255, blank=True)
    activation_phone_code = models.CharField(max_length=8, blank=True)
    is_active = models.BooleanField(default=False)
    is_phone_active = models.BooleanField(default=False)

    first_name = None
    last_name = None
    groups = None
    user_permissions = None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code

    def create_phone_activation_code(self):
        from random import randint
        code = randint(100000, 1000000)
        self.activation_phone_code = code





