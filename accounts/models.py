# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def get_username(self, email):
        try:
            username = self.normalize_email(email)
            return username.split('@')[0]
        except:
            return email

    def create_user(self, email, password, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            username=self.get_username(email),
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email,
            username=self.get_username(email),
            is_staff=True,
            is_superuser=True,
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

@python_2_unicode_compatible
class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    username = models.CharField("Username", max_length=200)
    email = models.EmailField("Email", unique=True)
    avatar = models.CharField("Avatar", default='', max_length=200)
    first_name = models.CharField("First name", max_length=200, default='')
    last_name = models.CharField("Last name", max_length=200, default='')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username or self.email