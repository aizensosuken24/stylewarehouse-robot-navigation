/**
 * API Communication Module
 * Handles all communication with the backend
 */

const API = {
    baseURL: '',
    
    /**
     * Check if the API is healthy
     */
    async health() {
        try {
            const response = await fetch(`${this.baseURL}/api/health`);
            return response.ok;
        } catch (error) {
            console.error('Health check failed:', error);
            return false;
        }
    },

    /**
     * Get the full product catalogue
     */
    async getCatalogue() {
        try {
            const response = await fetch(`${this.baseURL}/api/catalogue`);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Failed to fetch catalogue:', error);
            throw error;
        }
    },

    /**
     * Search the catalogue
     */
    async searchCatalogue(query, limit = 20) {
        try {
            const params = new URLSearchParams();
            if (query) params.append('search', query);
            if (limit) params.append('limit', limit);
            
            const response = await fetch(`${this.baseURL}/api/catalogue?${params}`);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Search failed:', error);
            throw error;
        }
    },

    /**
     * Get a specific product by ID
     */
    async getProduct(productId) {
        try {
            const response = await fetch(`${this.baseURL}/api/catalogue/${productId}`);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Failed to fetch product:', error);
            throw error;
        }
    },

    /**
     * Get a demo order
     */
    async getDemoOrder() {
        try {
            const response = await fetch(`${this.baseURL}/api/demo-order`);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Failed to fetch demo order:', error);
            throw error;
        }
    },

    /**
     * Simulate an order
     */
    async simulateOrder(items) {
        try {
            const response = await fetch(`${this.baseURL}/api/simulate-order`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ items }),
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Order simulation failed:', error);
            throw error;
        }
    },
};

/**
 * Utility function to format JSON for display
 */
function formatJSON(obj, indent = 2) {
    return JSON.stringify(obj, null, indent);
}

/**
 * Utility function to parse location string (e.g., "A1" or "B3")
 */
function parseLocation(location) {
    if (!location || typeof location !== 'string') return null;
    const match = location.match(/([A-Z])(\d+)/);
    if (!match) return null;
    return {
        row: match[1].charCodeAt(0) - 65, // Convert A=0, B=1, etc.
        col: parseInt(match[2], 10)
    };
}

/**
 * Utility function to format location back to string
 */
function formatLocation(row, col) {
    return String.fromCharCode(65 + row) + col;
}
