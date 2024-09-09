from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    """ User Profile MOdel """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length= 100, blank= True, default= None)
    last_name = models.CharField(max_length= 100, blank= True, default= None)
    national_id = models.CharField(max_length= 30 , blank= True, default=  None)
    contact1 = models.CharField(max_length=20)
    contact2 = models.CharField(max_length=20, blank=True, null=True)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f'Profile of {self.user.email}'
