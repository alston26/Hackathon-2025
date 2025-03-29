import random

def categorize_item(image_path):
    """
    Mock AI function to categorize an item based on its image.
    """
    categories = ['Electronics', 'Clothing', 'Books', 'Accessories', 'Other']
    category = random.choice(categories)
    confidence = random.uniform(0.7, 1.0)  # Mock confidence score between 70% and 100%
    return category, confidence

def rag_search(query, queryset):
    """
    Mock AI-powered search function.
    """
    # For simplicity, return the entire queryset as a mock result
    return queryset