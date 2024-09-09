from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

# custom imports
from .models import Bid
from bidding import  serializerz
from custom_auth.models import User
from notifications.models import Email
from animals.models import Animal


            
class BidListCreateAPIView(APIView):
    serializer_class = serializerz.BidSerializer
    
    def get(self, request):
        bids = Bid.objects.all()
        serializer = self.serializer_class(bids, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializer_class,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            user_id = request.data.get('user')  
            
            user_email = ""
            try:
                user = User.objects.get(pk=user_id)
                user_email = user.email
            except User.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
            # get animal details
            animal_id = request.data.get('animal')  

            try:
                animal = Animal.objects.get(pk=animal_id)

            except User.DoesNotExist:
                return Response({'error': 'Livestock Does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
            
            send_email_obj = Email()
            email_text = f"""
                         You have successfully bidded for animal. Here are the details of the animal:
                         Animal name: {animal.name} \n
                         Animal Breed: {animal.breed} \n
                         Animal Age: {animal.age} \n
                         Animal Weight: {animal.weight} in kgs \n
                         Animal Health Information: {animal.health_info} in kgs \n
                         \n\n
                         At the price of {request.data.get('price')}
                         
                         
                         
                         
                        """
            
            email =  user_email
            subject = "Successfully Bidded"
            send_email_obj.send_email(email, subject, email_text)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BidRetrieveUpdateDestroyAPIView(APIView):
    serializer_class = serializerz.BidSerializer
    @swagger_auto_schema(request_body=serializer_class,)
    def get_object(self, pk):
        try:
            return Bid.objects.get(pk=pk)
        except Bid.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        bid = self.get_object(pk)
        serializer = self.serializer_class(bid)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializer_class,)
    def put(self, request, pk):
        bid = self.get_object(pk)
        serializer = self.serializer_class(bid, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializer_class,)
    def delete(self, request, pk):
        bid = self.get_object(pk)
        bid.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
