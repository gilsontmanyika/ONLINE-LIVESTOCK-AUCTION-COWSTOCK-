# animals urls
from django.urls import path
from .views import AnimalListCreateView, AnimalRetrieveUpdateDestroyView

urlpatterns = [
    path('animals/', AnimalListCreateView.as_view(), name='animal-list-create'),
    path('animals/<int:pk>/', AnimalRetrieveUpdateDestroyView.as_view(), name='animal-retrieve-update-destroy'),
]
