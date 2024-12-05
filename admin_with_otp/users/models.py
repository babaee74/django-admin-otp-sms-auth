from multiprocessing.dummy import Value
from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import  gettext_lazy as _
import json
import uuid as uuid_


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile, password, **other_fields):
        
        if not mobile:
            raise ValueError(_('You need to provide a mobile number'))
        if not password:
            raise ValueError(_('You need to provide a password'))
        if not isinstance(password, str):
            raise ValueError(_('You need to provide a password'))
        
        
        # email = self.normalize_email(email)
        user =  self.model(mobile=mobile, **other_fields)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, mobile, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)
        return self.create_user(mobile, password, **other_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    # common fields
    mobile = models.CharField(unique=True, max_length=20)
    first_name = models.CharField(unique=False, blank=True, max_length=150)
    
    # status fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


    objects = CustomUserManager()
    
    USERNAME_FIELD = 'mobile' # ! important, changes the default username field for admin
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.mobile



        