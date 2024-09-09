from django.urls import path

from users import views


urlpatterns = [
    path('users/', views.UserProfileView.as_view(), name = 'User Profile'),
    
]