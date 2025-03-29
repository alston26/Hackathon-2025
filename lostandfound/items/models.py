from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    building = models.CharField(max_length=100, blank=True, null=True)
    floor = models.CharField(max_length=50, blank=True, null=True)
    room = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class LostItem(models.Model):
    STATUS_CHOICES = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='LOST')
    category = models.CharField(max_length=100)
    lost_location = models.ForeignKey(Location, related_name='lost_items', on_delete=models.CASCADE)
    found_location = models.ForeignKey(Location, related_name='found_items', on_delete=models.SET_NULL, blank=True, null=True)
    lost_time = models.DateTimeField(auto_now_add=True)
    found_time = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    ai_category = models.CharField(max_length=100, blank=True, null=True)
    ai_confidence = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class SearchQuery(models.Model):
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query