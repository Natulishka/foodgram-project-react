from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):
    '''
    При создании суперпользователя проставляет пользовательскую роль admin,
    не позволяет создать пользователя с username me, поля email, first_name, last_name
    обязательны для заполнения. Для суперпользователя генерируется токен.
    '''
    def create_user(self, username, email, password, first_name, last_name, superuser=False, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('Username must be set'))
        if username == 'me':
            raise ValueError(_("Username can't be 'me'"))
        if not first_name:
            raise ValueError(_('First name must be set'))
        if not last_name:
            raise ValueError(_('Last name must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username,
                          email=email,
                          first_name=first_name,
                          last_name=last_name,
                          **extra_fields)
        user.set_password(password)
        user.save()
        if superuser == True:
            token = Token.objects.create(user=user)
            print('Token ' + token.key)
        return user

    def create_superuser(self, username, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        superuser = True
        return self.create_user(username, email, password, first_name, last_name, superuser, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        max_length=254,
        unique=True)
    password = models.CharField(
        _('password'),
        max_length=150)
    first_name = models.CharField(
        _('first name'),
        max_length=150)
    last_name = models.CharField(
        _('last name'),
        max_length=150)
    # is_subscribed = models.BooleanField(
    #     _('is subscribed'),
    #     default=False,
    # )
    
    objects = CustomUserManager()
    
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'is_subscribed']
    USERNAME_FIELD = 'email'
    
    class Meta:
        ordering = ['pk']
