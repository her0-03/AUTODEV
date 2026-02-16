// API Helper - Toutes les requêtes passent par le backend Flask
const API = {
    // Base URL - toujours relatif au frontend
    baseURL: '/api',
    
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
        
        // Ne pas ajouter Content-Type pour FormData
        if (options.body instanceof FormData) {
            delete config.headers['Content-Type'];
        }
        
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
        return this.request('/projects', {
            method: 'POST',
            body: JSON.stringify({ name, description })
        });
    },
    
    async uploadFiles(files) {
        const formData = new FormData();
        for (let file of files) {
            formData.append('files', file);
        }
        
        return this.request('/upload', {
            method: 'POST',
            body: formData
        });
    },
    
    async createJob(projectId, inputFiles) {
        return this.request('/generation/job', {
            method: 'POST',
            body: JSON.stringify({ project_id: projectId, input_files: inputFiles })
        });
    },
    
    async saveSpec(jobId, spec) {
        return this.request(`/generation/job/${jobId}/save-spec`, {
            method: 'POST',
            body: JSON.stringify(spec)
        });
    },
    
    async generateCode(jobId) {
        return this.request(`/generation/job/${jobId}/generate`, {
            method: 'POST'
        });
    }
};

// Export global
window.API = API;
