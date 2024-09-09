from rest_framework import serializers
from .models import Animal, AnimalImage
from bidding.models import Bid

class AnimalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalImage
        fields = ('image',)

class AnimalSerializer(serializers.ModelSerializer):
    images = AnimalImageSerializer(many=True, read_only=True)

    class Meta:
        model = Animal
        fields = '__all__'
    
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        last_bid = Bid.objects.filter(animal=instance).order_by('-date').first()
        if last_bid:
            data['lastprice'] = float(last_bid.price)
        else:
            data['lastprice'] = float(instance.price)
        return data
