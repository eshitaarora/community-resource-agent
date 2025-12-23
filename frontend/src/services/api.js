import axios from 'axios';

const API_BASE_URL = import.meta.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat Service
export const chatService = {
  sendMessage: async (userId, message, userContext = null) => {
    const response = await apiClient.post('/chat/send', {
      user_id: userId,
      message,
      user_context: userContext,
    });
    return response.data;
  },

  getHistory: async (userId, limit = 10) => {
    const response = await apiClient.get(`/chat/history/${userId}`, {
      params: { limit },
    });
    return response.data;
  },

  clearHistory: async (userId) => {
    const response = await apiClient.delete(`/chat/history/${userId}`);
    return response.data;
  },

  submitFeedback: async (messageId, helpful, feedbackText = null) => {
    const response = await apiClient.post(`/chat/feedback/${messageId}`, {
      helpful,
      feedback_text: feedbackText,
    });
    return response.data;
  },
};

// Resources Service
export const resourcesService = {
  listResources: async (category = null, skip = 0, limit = 50) => {
    const response = await apiClient.get('/resources/', {
      params: { category, skip, limit },
    });
    return response.data;
  },

  getResource: async (serviceId) => {
    const response = await apiClient.get(`/resources/${serviceId}`);
    return response.data;
  },

  searchNearby: async (latitude, longitude, radiusMiles = 5, category = null) => {
    const response = await apiClient.get('/resources/search/nearby', {
      params: {
        latitude,
        longitude,
        radius_miles: radiusMiles,
        category,
      },
    });
    return response.data;
  },

  searchLocations: async (query) => {
    const response = await apiClient.get('/resources/search/locations', {
      params: { query },
    });
    return response.data;
  },

  getByCategory: async (categoryName, skip = 0, limit = 50) => {
    const response = await apiClient.get(`/resources/category/${categoryName}`, {
      params: { skip, limit },
    });
    return response.data;
  },

  verifyService: async (serviceId) => {
    const response = await apiClient.post(`/resources/${serviceId}/verify`);
    return response.data;
  },
};

// Analytics Service
export const analyticsService = {
  getDashboardStats: async (days = 30) => {
    const response = await apiClient.get('/analytics/stats', {
      params: { days },
    });
    return response.data;
  },

  getUserImpact: async (days = 30) => {
    const response = await apiClient.get('/analytics/impact/users', {
      params: { days },
    });
    return response.data;
  },

  getServiceImpact: async (days = 30) => {
    const response = await apiClient.get('/analytics/impact/services', {
      params: { days },
    });
    return response.data;
  },

  getCategoryImpact: async (days = 30) => {
    const response = await apiClient.get('/analytics/impact/categories', {
      params: { days },
    });
    return response.data;
  },

  logServiceAccess: async (userId, serviceId, serviceName, contactMethod, outcome = null, notes = null) => {
    const response = await apiClient.post('/analytics/service-access', {
      user_id: userId,
      service_id: serviceId,
      service_name: serviceName,
      contact_method: contactMethod,
      outcome,
      notes,
    });
    return response.data;
  },
};

export default apiClient;
