/* API Client */
class APIClient {
    constructor(baseURL = 'http://localhost:5001/api') {
        this.baseURL = baseURL;
        this.token = localStorage.getItem('auth_token');
    }

    setToken(token) {
        this.token = token;
        localStorage.setItem('auth_token', token);
    }

    clearToken() {
        this.token = null;
        localStorage.removeItem('auth_token');
    }

    getHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        };
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }

    async request(method, endpoint, data = null) {
        const url = `${this.baseURL}${endpoint}`;
        const options = {
            method,
            headers: this.getHeaders()
        };

        if (data && (method === 'POST' || method === 'PUT')) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            
            if (response.status === 401) {
                this.clearToken();
                window.location.href = '/';
            }

            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Error en la solicitud');
            }

            return result;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Auth endpoints
    async register(email, username, password, full_name = '') {
        return this.request('POST', '/auth/register', {
            email,
            username,
            password,
            full_name
        });
    }

    async login(email, password) {
        return this.request('POST', '/auth/login', { email, password });
    }

    async getCurrentUser() {
        return this.request('GET', '/auth/me');
    }

    async logout() {
        return this.request('POST', '/auth/logout');
    }

    // Properties endpoints
    async getProperties(filters = {}) {
        const params = new URLSearchParams();
        Object.keys(filters).forEach(key => {
            if (filters[key]) params.append(key, filters[key]);
        });
        return this.request('GET', `/properties?${params.toString()}`);
    }

    async getProperty(id) {
        return this.request('GET', `/properties/${id}`);
    }

    async createProperty(propertyData) {
        return this.request('POST', '/properties', propertyData);
    }

    // AI Search
    async aiSearch(query) {
        return this.request('POST', '/ai/search', { query });
    }

    // Agents
    async getAgents() {
        return this.request('GET', '/ai/agents');
    }

    async executeAgent(agentName, task, context = null) {
        return this.request('POST', `/ai/agent/${agentName}`, { task, context });
    }

    // RAG
    async ragSearch(query, top_k = 5) {
        return this.request('POST', '/rag/search', { query, top_k });
    }

    // Documents
    async uploadDocument(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const options = {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.token}`
            },
            body: formData
        };

        const response = await fetch(`${this.baseURL}/documents/upload`, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Error subiendo documento');
        }

        return result;
    }

    async processDocuments() {
        return this.request('POST', '/documents/process');
    }

    // Favorites
    async getFavorites() {
        return this.request('GET', '/favorites');
    }

    async addFavorite(propertyId) {
        return this.request('POST', `/favorites/${propertyId}`);
    }

    async removeFavorite(propertyId) {
        return this.request('DELETE', `/favorites/${propertyId}`);
    }

    // Health Check
    async healthCheck() {
        return this.request('GET', '/health');
    }
}

// Crear instancia global
const apiClient = new APIClient();
