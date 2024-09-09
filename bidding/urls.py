# animals urls
from django.urls import path
from .views import BidListCreateAPIView, BidRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('bid/', BidListCreateAPIView.as_view(), name='bid-list-create'),
    path('bid/<int:pk>/', BidRetrieveUpdateDestroyAPIView.as_view(), name='bid-retrieve-update-destroy'),
]
