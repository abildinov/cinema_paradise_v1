// API Configuration
const API_BASE_URL = 'http://192.168.0.10:8000';

// Axios instance with base configuration
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    }
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            // Не перезагружаем сразу, позволяем компонентам обработать ошибку
            // window.location.reload();
        }
        return Promise.reject(error);
    }
);

// API Service
window.api = {
    // Внутренние методы
    async _request(method, url, data = null, options = {}) {
        try {
            const response = await api({
                method,
                url,
                data,
                ...options
            });
            return response.data;
        } catch (error) {
            console.error(`API Error [${method} ${url}]:`, error);
            
            if (error.response?.status === 401) {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                // Генерируем событие для обновления UI
                window.dispatchEvent(new CustomEvent('authError'));
            }
            
            const message = error.response?.data?.detail || error.message || 'Произошла ошибка';
            throw new Error(message);
        }
    },

    // Публичные методы
    // Health check
    async health() {
        return await this._request('GET', '/health');
    },

    // Demo data population
    async populateDemo() {
        return await this._request('GET', '/demo/populate');
    },

    // Authentication
    async login(username, password) {
        // Для form-data
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
    
        const response = await api.post('/auth/login', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });
    
        if (response.data.access_token) {
            localStorage.setItem('token', response.data.access_token);
    
            // Получаем полную информацию о пользователе из /auth/me
            try {
                const userInfo = await this.getCurrentUser();
                localStorage.setItem('user', JSON.stringify(userInfo));
                return { ...response.data, user: userInfo };
            } catch (e) {
                console.error('Failed to get user info after login:', e);
                localStorage.removeItem('token');
                throw new Error('Не удалось получить информацию о пользователе');
            }
        }
    
        return response.data;
    },

    async register(userData) {
        const response = await this._request('POST', '/auth/register', userData);
        
        // Автоматически логинимся после регистрации
        if (response.username) {
            return await this.login(userData.username, userData.password);
        }
        
        return response;
    },

    async getCurrentUser() {
        return await this._request('GET', '/auth/me');
    },

    // Movies
    async getMovies(skip = 0, limit = 100) {
        return await this._request('GET', `/movies?skip=${skip}&limit=${limit}`);
    },

    async getMovie(movieId) {
        return await this._request('GET', `/movies/${movieId}`);
    },

    // Sessions
    async getSessions(skip = 0, limit = 100) {
        return await this._request('GET', `/sessions?skip=${skip}&limit=${limit}`);
    },

    async getCinemas() {
        return this._request('GET', '/cinemas?skip=0&limit=100');
    },

    // Tickets
    async createTicket(ticketData) {
        return await this._request('POST', '/tickets', ticketData);
    },

    async getUserTickets() {
        return await this._request('GET', '/tickets/my');
    },

    async getTicketsForSession(sessionId) {
        return await this._request('GET', `/sessions/${sessionId}/tickets`);
    },

    // Admin endpoints
    async getAllTickets() {
        return this._request('GET', '/admin/tickets?skip=0&limit=100');
    },

    async getAllUsers() {
        return this._request('GET', '/admin/users?skip=0&limit=100');
    },

    // Demo endpoint
};

// Utility functions
// Утилиты для аутентификации
window.AuthUtils = {
    isAuthenticated() {
        return !!localStorage.getItem('token');
    },

    getCurrentUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.reload();
    },

    isAdmin() {
        const user = this.getCurrentUser();
        return user && user.role === 'admin';
    }
};

// Обработчик события authError для автоматического выхода
window.addEventListener('authError', () => {
    if (window.AuthUtils.isAuthenticated()) {
        window.AuthUtils.logout();
    }
});

// Создаем глобальный алиас для обратной совместимости
window.ApiService = window.api;

console.log('🔌 API Service загружен');