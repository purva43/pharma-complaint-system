import api from './axios';

export const complaintsAPI = {
  list: async (params = {}) => {
    const response = await api.get('/complaints', { params });
    return response.data;
  },

  get: async (id) => {
    const response = await api.get(`/complaints/${id}`);
    return response.data;
  },

  create: async (data) => {
    const response = await api.post('/complaints', data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await api.put(`/complaints/${id}`, data);
    return response.data;
  },

  delete: async (id) => {
    await api.delete(`/complaints/${id}`);
  },

  processAI: async (id) => {
    const response = await api.post(`/complaints/${id}/ai`);
    return response.data;
  },
};
