# items/views.py
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import LostItem, Location, SearchQuery
from .serializers import LostItemSerializer, LocationSerializer
from .ai_utils import rag_search
from django.shortcuts import render
from django.http import HttpResponse  # Removed unused import
from django.shortcuts import render
# Removed unused import of HttpResponse

class LostItemListCreate(generics.ListCreateAPIView):
    queryset = LostItem.objects.all()
    serializer_class = LostItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'category', 'lost_location', 'found_location']
    search_fields = ['title', 'description', 'category']
    
    def perform_create(self, serializer):
        item = serializer.save(user=self.request.user)
        # Process image in background
        try:
            try:
                from .tasks import process_item_image
            except ImportError:
                raise ImportError("The 'tasks' module could not be found. Ensure 'tasks.py' exists in the correct directory or update the import path.")
        except ImportError:
            raise ImportError("The 'tasks' module could not be found. Ensure 'tasks.py' exists in the same directory as 'views.py'.")
        process_item_image.delay(item.id)

class LocationListView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class SearchView(generics.ListAPIView):
    serializer_class = LostItemSerializer
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')  # Ensure proper indentation
        is_rag = self.request.GET.get('rag', 'false').lower() == 'true'
        location_filter = self.request.GET.get('location')
        time_filter = self.request.GET.get('time')
        
        # Save search query
        if self.request.user.is_authenticated:
            SearchQuery.objects.create(
                user=self.request.user,
                query_text=query,
                filters={
                    'location': location_filter,
                    'time': time_filter,
                    'is_rag': is_rag
                }
            )
        
        queryset = LostItem.objects.all()
        
        if location_filter:
            queryset = queryset.filter(lost_location_id=location_filter)
        
        if time_filter:
            # Implement time filtering logic
            pass
            
        if is_rag:
            return rag_search(query, queryset)
        else:
            if query:
                return queryset.filter(
                    title__icontains=query
                ) | queryset.filter(
                    description__icontains=query
                ) | queryset.filter(
                    category__icontains=query
                )
            return queryset

def index(request):
    return render(request, 'items/base.html')  # Render the base template or a custom homepage template

def submit_item(request):
    return render(request, 'items/submission.html')  # Render the submission template