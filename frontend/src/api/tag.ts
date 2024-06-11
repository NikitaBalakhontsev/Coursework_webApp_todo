// src/api/tag.ts
import axios from 'axios';
import { getToken } from '../stores/authStore';

const tagAPI = axios.create({
  baseURL: 'http://176.53.160.126:8000/api'
});

tagAPI.interceptors.request.use(config => {
  const token = getToken();
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});


