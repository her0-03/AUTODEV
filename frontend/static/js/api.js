// API Helper - Toutes les requêtes passent par le backend Flask
const API = {
    // Base URL - toujours relatif au frontend
    baseURL: '/api',
    
    // Helper pour faire des requêtes avec retry
    async request(endpoint, options = {}, retries = 3) {
        const url = `${this.baseURL}${endpoint}`;
        console.log(`[API] Request: ${options.method || 'GET'} ${url}`);
        
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
        
        for (let i = 0; i < retries; i++) {
            try {
                console.log(`[API] Attempt ${i+1}/${retries}`);
                const response = await fetch(url, config);
                console.log(`[API] Response status: ${response.status}`);
                
                const data = await response.json();
                console.log(`[API] Response data:`, data);
                
                if (!response.ok) {
                    // Si 503 (backend endormi), retry après 5 secondes
                    if (response.status === 503 && i < retries - 1) {
                        console.log(`[API] Backend endormi, retry ${i+1}/${retries} dans 5s...`);
                        await new Promise(resolve => setTimeout(resolve, 5000));
                        continue;
                    }
                    throw new Error(data.error || data.detail || 'Erreur réseau');
                }
                
                return data;
            } catch (error) {
                console.error(`[API] Error on attempt ${i+1}:`, error);
                if (i === retries - 1) {
                    throw error;
                }
                console.log(`[API] Retrying in 2s...`);
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
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
