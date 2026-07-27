import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  complaints: [],
  currentComplaint: null,
  loading: false,
  error: null,
  filters: {
    status: '',
    priority: '',
    risk_level: '',
    category: '',
  },
  pagination: {
    page: 1,
    pageSize: 10,
    total: 0,
  },
};

const complaintSlice = createSlice({
  name: 'complaints',
  initialState,
  reducers: {
    setComplaints: (state, action) => {
      state.complaints = action.payload.items;
      state.pagination.total = action.payload.total;
      state.pagination.page = action.payload.page;
      state.pagination.pageSize = action.payload.page_size;
    },
    setCurrentComplaint: (state, action) => {
      state.currentComplaint = action.payload;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
    },
    setFilters: (state, action) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    clearFilters: (state) => {
      state.filters = initialState.filters;
    },
    addComplaint: (state, action) => {
      state.complaints.unshift(action.payload);
    },
    updateComplaint: (state, action) => {
      const index = state.complaints.findIndex(c => c.id === action.payload.id);
      if (index !== -1) {
        state.complaints[index] = action.payload;
      }
      if (state.currentComplaint?.id === action.payload.id) {
        state.currentComplaint = action.payload;
      }
    },
    deleteComplaint: (state, action) => {
      state.complaints = state.complaints.filter(c => c.id !== action.payload);
      if (state.currentComplaint?.id === action.payload) {
        state.currentComplaint = null;
      }
    },
  },
});

export const {
  setComplaints,
  setCurrentComplaint,
  setLoading,
  setError,
  setFilters,
  clearFilters,
  addComplaint,
  updateComplaint,
  deleteComplaint,
} = complaintSlice.actions;

export default complaintSlice.reducer;
