# items/tasks.py
from celery import shared_task
from django.core.files.storage import default_storage
from .models import LostItem
from .ai_utils import categorize_item
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def process_item_image(self, item_id):
    """
    Background task to process item image and categorize it using AI
    """
    try:
        item = LostItem.objects.get(id=item_id)
        
        if not item.image:
            logger.warning(f"No image found for item {item_id}")
            return
            
        # Get the absolute path to the image
        image_path = default_storage.path(item.image.name)
        
        # Get AI categorization
        category, confidence = categorize_item(image_path)
        
        if category:
            # Update the item with AI results
            LostItem.objects.filter(id=item_id).update(
                ai_category=category,
                ai_confidence=confidence
            )
            logger.info(f"Successfully processed image for item {item_id}. Category: {category}, Confidence: {confidence}")
        else:
            logger.warning(f"AI failed to categorize image for item {item_id}")
            
    except LostItem.DoesNotExist:
        logger.error(f"LostItem {item_id} does not exist")
        raise self.retry(countdown=60 * 5)  # Retry in 5 minutes
        
    except Exception as e:
        logger.error(f"Error processing image for item {item_id}: {str(e)}")
        raise self.retry(exc=e, countdown=60 * 2)  # Retry in 2 minutes

@shared_task
def cleanup_unclaimed_items():
    """
    Periodic task to clean up old unclaimed items
    """
    from django.utils import timezone
    from datetime import timedelta
    
    threshold = timezone.now() - timedelta(days=90)  # 3 months old
    unclaimed_items = LostItem.objects.filter(
        status='FOUND',
        found_time__lte=threshold
    )
    
    count = unclaimed_items.count()
    unclaimed_items.delete()
    
    logger.info(f"Cleaned up {count} unclaimed items older than 90 days")