// Main JavaScript for AutoDev Frontend

document.addEventListener('DOMContentLoaded', function() {
    console.log('AutoDev Frontend Loaded');
});

// Utility function for API calls
async function apiCall(endpoint, method = 'GET', body = null) {
    const token = sessionStorage.getItem('token');
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const options = {
        method,
        headers
    };
    
    if (body) {
        options.body = JSON.stringify(body);
    }
    
    const response = await fetch(`http://localhost:8000${endpoint}`, options);
    return response.json();
}
