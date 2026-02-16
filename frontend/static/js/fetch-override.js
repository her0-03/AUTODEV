// Global API URL helper
window.getApiUrl = function(path) {
    // Remplacer localhost:8000/api/v1 par /api (proxy Flask)
    return path.replace('http://localhost:8000/api/v1', '/api');
};

// Override fetch pour remplacer automatiquement les URLs
const originalFetch = window.fetch;
window.fetch = function(url, options) {
    if (typeof url === 'string' && url.includes('localhost:8000')) {
        url = url.replace('http://localhost:8000/api/v1', '/api');
        console.log('[FETCH OVERRIDE] Redirected to:', url);
    }
    return originalFetch(url, options);
};

console.log('[API HELPER] Fetch override active - all localhost:8000 calls will use proxy');
