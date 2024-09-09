#buildint imports
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
import decimal

#custom imports
from .models import Animal, AnimalImage
from bidding.models import Bid
from animals import serializers
from notifications.models import Email
from custom_auth.models import User


class AnimalListCreateView(APIView):
    serializer_class = serializers.AnimalSerializer
    parser_classes = [MultiPartParser, FormParser]  # Allow file uploads

    """ Animal List API View """

    def get(self, request, format=None):
        animals = Animal.objects.all()
        serializer = self.serializer_class(animals, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializer_class,)
    def post(self, request, format=None):
        print(f"Printing images received: {request.data}")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            animal = serializer.save()

            # Save uploaded images
            images_data = request.FILES.getlist('pictures')  # Access all images

            for image_data in images_data:
                print("Saving image...")
                AnimalImage.objects.create(animal=animal, image=image_data)
            
            #get user email
            user_id = request.data.get('user')  
            user_email = ""
            try:
                user = User.objects.get(pk=user_id)
                user_email = user.email
            except User.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
            # get user email from 
            
            send_email_obj = Email()
            email_text = f"""
                         You have successfully added a livestock. Here are the details of the livestock:
                         {serializer.data}
                         
                        """
            
            email =  user_email
            subject = "Successfully Added Animal"
            send_email_obj.send_email(email, subject, email_text)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AnimalRetrieveUpdateDestroyView(APIView):
    serializer_class = serializers.AnimalSerializer
    @swagger_auto_schema(request_body=serializer_class,)
    def get_object(self, pk):
        """ Get Animal by id """
        try:
            animal_data = Animal.objects.get(pk=pk)
            print(f"The animal data is as follows {animal_data.name}")
            last_bid = Bid.objects.filter(animal_id=pk).order_by('-date').first()
            if last_bid:
                animal_data.lastprice = float(last_bid.price)
            else:
                animal_data.lastprice = float(animal_data.price)
            print(f"The animal last price is: {animal_data.lastprice}")
            print(f"The animal last price is: {type(animal_data)}")

            return animal_data
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
