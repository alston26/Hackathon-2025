// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Form submission for lost items
    const itemForm = document.getElementById('item-form');
    if (itemForm) {
        itemForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData();
            formData.append('title', document.getElementById('title').value);
            formData.append('description', document.getElementById('description').value);
            formData.append('category', document.getElementById('category').value);
            formData.append('lost_location', document.getElementById('lost-location').value);
            formData.append('image', document.getElementById('image').files[0]);
            
            try {
                const response = await axios.post('/api/items/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                });
                window.location.href = `/item/${response.data.id}`;
            } catch (error) {
                console.error('Error submitting item:', error);
                alert('Error submitting item. Please try again.');
            }
        });
    }
    
    // Image preview and AI category suggestion
    const imageInput = document.getElementById('image');
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    document.getElementById('image-preview').src = event.target.result;
                    document.getElementById('image-preview').classList.remove('hidden');
                    
                    // Send to AI for category suggestion
                    suggestCategory(file);
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    async function suggestCategory(imageFile) {
        const formData = new FormData();
        formData.append('image', imageFile);
        
        try {
            const response = await axios.post('/api/ai/suggest-category/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            
            if (response.data.category) {
                document.getElementById('category').value = response.data.category;
                document.getElementById('ai-suggestion').classList.remove('hidden');
                document.getElementById('ai-category').textContent = response.data.category;
                document.getElementById('ai-confidence').textContent = 
                    (response.data.confidence * 100).toFixed(1) + '%';
            }
        } catch (error) {
            console.error('AI suggestion error:', error);
        }
    }
    
    function getCookie(name) {
        // Standard Django CSRF token cookie retrieval
    }
});