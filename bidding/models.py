import decimal
from django.db import models
from animals.models import Animal
from django.conf import settings


class Bid(models.Model):
    """Bidding Model """
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name= 'userbidding')
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)

    def calculate_price(self):
        previous_bid = Bid.objects.filter(animal=self.animal).order_by('-date').first()
        if previous_bid:
            max_allowed_price = previous_bid.price * decimal.Decimal(1.35)  # 35% greater than the previous bid price
            min_allowed_price = previous_bid.price + decimal.Decimal('0.01')  # Ensure bid is greater than the previous bid price
            if min_allowed_price < self.price <= max_allowed_price:
                return self.price
            elif self.price <= min_allowed_price:
                return min_allowed_price
            else:
                return max_allowed_price
        return self.price


    def save(self, *args, **kwargs):
        self.price = self.calculate_price()
        super().save(*args, **kwargs)
        

    def __str__(self):
        return f"Bid for Animal {self.animal_id} by User {self.user_id}"
