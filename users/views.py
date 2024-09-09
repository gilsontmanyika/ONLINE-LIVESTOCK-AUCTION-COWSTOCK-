from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from .serializers import UserProfileSerializer
from users.models import UserProfile

class UserProfileView(APIView):
    """ User Profile : """
    serializer_class = UserProfileSerializer
    
    @swagger_auto_schema(request_body=serializer_class,)
    def post(self, request, format='json'):
        #add new user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @swagger_auto_schema()
    def get(self, request, format=None):
        profiles = UserProfile.objects.all()
        serializer = self.serializer_class(profiles, many=True)
        return Response(serializer.data)


""" To be added later ons
class UserProfileRetriveUpdate(APIView):
    serializer_class = serializers.AnimalSerializer
    @swagger_auto_schema(request_body=serializer_class,)
    def get_object(self, pk):
  
        try:
            return Animal.objects.get(pk=pk)
        except Animal.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk, format=None):

        animal = self.get_object(pk)
        serializer = self.serializer_class(animal)
        # serializer = AnimalSerializer(animal)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializer_class,)
    def put(self, request, pk, format=None):
        animal = self.get_object(pk)
        # serializer = AnimalSerializer(animal, data=request.data)
        serializer = self.serializer_class(animal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializer_class,)
    def delete(self, request, pk, format=None):
        animal = self.get_object(pk)
        animal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    """
    




    
