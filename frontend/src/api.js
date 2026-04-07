// src/api.js
import axios from 'axios';

const API_BASE = 'https://voter-registration-gn1a.onrender.com/api';  // uses proxy (see package.json later)

export const registerViaWeb = (data) => axios.post(`${API_BASE}/register/web/`, data);
export const fetchApplicants = () => axios.get(`${API_BASE}/applicants/`);