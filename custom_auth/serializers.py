from rest_framework import serializers

from custom_auth import models

class UserAuthSerializer(serializers.ModelSerializer):
    """ UserAuth serialiser """
    class Meta:
        model = models.User
        fields = ('id', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }