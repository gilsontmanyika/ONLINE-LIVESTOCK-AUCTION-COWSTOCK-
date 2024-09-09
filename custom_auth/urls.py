from django.urls import path

from custom_auth import views


urlpatterns = [
    path('api-token-auth/', views.AuthView.as_view(), name = 'Auth'),
    
]