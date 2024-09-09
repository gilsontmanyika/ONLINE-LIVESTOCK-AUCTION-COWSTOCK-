from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from custom_auth import serializers

class AuthView(APIView):
    serializer_class = serializers.UserAuthSerializer
    """ API VIEW FOR LOGIN """
    @swagger_auto_schema(request_body=serializer_class,)
    def post(self, request):
        """ Login Method"""
        username = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username= username, password = password)
        if user :
            refresh = RefreshToken.for_user(user)
            return JsonResponse({'status': status.HTTP_200_OK ,'refresh': str(refresh), 'access': str(refresh.access_token)})
        else:
            return JsonResponse({'status': status.HTTP_401_UNAUTHORIZED, 'message': 'Wrong username or password'})

