from rest_framework import serializers
from custom_auth.serializers import UserAuthSerializer
#fetch from custom users model
from custom_auth.models import UserManager
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserAuthSerializer()  # Use the UserAuthSerializer for the user field

    class Meta:
        model = UserProfile
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        print(f"The user data is as follows ==>> {user_data} \n and  type is {type(user_data)}")
        #user_data.set_password(user_data['password'])
    
      
        
        # Create user using the manager instance
        #user_instance = user_manager.create_user(email=user_data['email'], password=user_data['password'])
        user_manager_obj = UserManager()
        
        user_instance = user_manager_obj.create_other_users(user_data['email'], user_data['password'])
        #user_instance = UserAuthSerializer.create(UserAuthSerializer(), validated_data=user_data)
        print(f"The value of saved data is {user_instance}")
        
        # Create profile instance with the created user and remaining data
        #profile_instance = UserProfile.objects.create(user=user_instance, **validated_data)
        profile_instance = UserProfile.objects.create(user=user_instance, **validated_data)
        
        
        return profile_instance
