from django.db import models
from .user_manager import User_Manager
from datetime import date
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _ ## this import is for auto translating
from django.utils import timezone
from datetime import date
import uuid

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('user name'), max_length=30, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    disabled_at = models.DateTimeField(null=True)

    objects = User_Manager()

    # use email as the username field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']