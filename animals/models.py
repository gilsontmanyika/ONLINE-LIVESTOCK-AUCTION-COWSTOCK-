from django.db import models
from django.conf import settings


class Animal(models.Model):
    """" Livestock Model """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='animals', default=1)
    name = models.CharField(max_length=250, blank=False)
    breed = models.CharField(max_length=250, blank=False)
    age = models.IntegerField(blank=False)
    weight = models.FloatField(blank=False)
    gender = models.CharField(max_length=10)
    health_info = models.TextField(blank=False)
    color = models.CharField(max_length=30, blank=False)
    video = models.CharField(blank=True, default="", max_length=100)
    price = models.FloatField(default= 100)
    status = models.BooleanField(default=True)

class AnimalImage(models.Model):
    """ Animal Image Model """
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='animal_images')

    def __str__(self):
        return f"Image of {self.animal.name}"

