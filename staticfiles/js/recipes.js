document.addEventListener('DOMContentLoaded', function() {
    // Ingredient search functionality
    const ingredientInputs = document.querySelectorAll('.ingredient-search');
    
    ingredientInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            const query = e.target.value.trim();
            if (query.length < 2) return;
            
            fetch('/api/ingredients/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: `q=${encodeURIComponent(query)}`
            })
            .then(response => response.json())
            .then(data => {
                console.log('Results:', data); 
            });
        });
    });
    
    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});