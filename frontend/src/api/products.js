import api from './axios';

export const productsAPI = {
  list: async (params = {}) => {
    const response = await api.get('/products', { params });
    return response.data;
  },

  get: async (id) => {
    const response = await api.get(`/products/${id}`);
    return response.data;
  },

  create: async (data) => {
    const response = await api.post('/products', data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await api.put(`/products/${id}`, data);
    return response.data;
  },
};
