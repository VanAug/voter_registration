import axios from 'axios';

const API_BASE = 'https://voter-registration-gn1a.onrender.com/api';
const ADMIN_TOKEN_KEY = 'adminToken';

const authHeaders = () => {
  const token = localStorage.getItem(ADMIN_TOKEN_KEY);
  return token ? { Authorization: `Token ${token}` } : {};
};

export const registerViaWeb = (data) => axios.post(`${API_BASE}/register/web/`, data);

export const loginAdmin = (credentials) => axios.post(`${API_BASE}/auth/admin-login/`, credentials);

export const fetchApplicants = () => axios.get(`${API_BASE}/applicants/`, { headers: authHeaders() });

export const deleteApplicant = (id) =>
  axios.delete(`${API_BASE}/applicants/${id}/`, { headers: authHeaders() });

export const setAdminToken = (token) => localStorage.setItem(ADMIN_TOKEN_KEY, token);

export const clearAdminToken = () => localStorage.removeItem(ADMIN_TOKEN_KEY);

export const isAdminLoggedIn = () => Boolean(localStorage.getItem(ADMIN_TOKEN_KEY));