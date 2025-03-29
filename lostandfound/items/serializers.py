from rest_framework import serializers  # Ensure the 'djangorestframework' package is installed
from .models import LostItem, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'building', 'floor', 'room']

class LostItemSerializer(serializers.ModelSerializer):
    lost_location = LocationSerializer(read_only=True)
    found_location = LocationSerializer(read_only=True)
    
    # For writable nested representation
    lost_location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        source='lost_location',
        write_only=True
    )
    
    found_location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        source='found_location',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = LostItem
        fields = [
            'id',
            'title',
            'description',
            'status',
            'category',
            'lost_location',
            'found_location',
            'lost_location_id',
            'found_location_id',
            'lost_time',
            'found_time',
            'image',
            'ai_category',
            'ai_confidence'
        ]
        read_only_fields = ['lost_time', 'ai_category', 'ai_confidence']