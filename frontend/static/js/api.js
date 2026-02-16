// API Helper - Toutes les requêtes passent par le backend Flask
const API = {
    // Base URL - toujours relatif au frontend
    baseURL: '',
    
    // Helper pour faire des requêtes
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        };
        
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || data.detail || 'Erreur réseau');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    // Projets
    async createProject(name, description) {
        return this.request('/api/create-project', {
            method: 'POST',
            body: JSON.stringify({ name, description })
        });
    },
    
    async uploadFiles(projectId, files) {
        const formData = new FormData();
        formData.append('project_id', projectId);
        for (let file of files) {
            formData.append('files', file);
        }
        
        return fetch('/api/upload-files', {
            method: 'POST',
            body: formData
        }).then(r => r.json());
    },
    
    async analyzeProject(jobId) {
        return this.request('/api/analyze', {
            method: 'POST',
            body: JSON.stringify({ job_id: jobId })
        });
    },
    
    async generateProject(jobId, spec) {
        return this.request('/api/generate', {
            method: 'POST',
            body: JSON.stringify({ job_id: jobId, spec })
        });
    }
};

// Export global
window.API = API;
