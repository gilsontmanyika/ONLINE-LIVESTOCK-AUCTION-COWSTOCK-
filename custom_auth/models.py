from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager



class UserManager(BaseUserManager):
    """ Manager for users """

    def create_user(self, email, password = None):
        """ Create a new user account """
        
        if not email:
            raise ValueError("Users must have email address")
        
        email = self.normalize_email(email)

        user = self.model(email = email)
        user.set_password(password)
        user.save(using= self._db)

        return user
    
    def create_other_users(self, email , password = None ):
        """ Create new user"""
        if not email:
            raise ValueError("Users must have email address")
        
        user = User()
        user.email= self.normalize_email(email= email)
        user.set_password(password)
        user.is_superuser = False
        user.is_staff = True

        user.save(using= self._db)
        return user
    
    
    
    def create_superuser(self, email , password ):
        """ Create a new super user """
        user = self.create_user(email , password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using= self._db)
        return user






class User(AbstractBaseUser, PermissionsMixin):
    """ Database model for users/ Auth in the system """
    email = models.EmailField(max_length = 255, unique = True)
    is_active = models.BooleanField(default= True)
    is_staff = models.BooleanField(default = False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email',]


    def get_full_name(self):
        """ Retrieves the email/ username of the user """
        return f"{self.email} "
    

    def __str__(self):
        """ Retrives string representation of a user """
        return f"{self.email} "




