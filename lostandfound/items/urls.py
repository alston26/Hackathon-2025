# filepath: /Users/alston/Desktop/Hackathon 2025/lostandfound/items/urls.py
from django.urls import path
from .views import LostItemListCreate, LocationListView, SearchView, index, submit_item

urlpatterns = [
    path('items/', LostItemListCreate.as_view(), name='item-list-create'),
    path('locations/', LocationListView.as_view(), name='location-list'),
    path('search/', SearchView.as_view(), name='search'),
    path('', index, name='index'),
    path('submit/', submit_item, name='submit-item'),
]