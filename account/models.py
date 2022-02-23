from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, name, phone_number, password=None):
        """
        Creates and saves a User with the given email, login
        name, phone_number, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not phone_number:
            raise ValueError('Users must have a phone_number')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone_number, password=None):
        """
        Creates and saves a superuser with the given email, name
        login, phone_number and password.
        """
        user = self.create_user(
            email=email,
            name=name,
            password=password,
            phone_number=phone_number
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    the model describing the user
    """

    name = models.CharField(max_length=125)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return self.login

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin