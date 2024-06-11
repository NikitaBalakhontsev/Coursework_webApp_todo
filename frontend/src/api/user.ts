// src/api/user.ts
import axios from 'axios';
import { getToken} from '../stores/authStore';
const userAPI = axios.create({
  baseURL: 'http://127.0.0.1:8000/api'
});

userAPI.interceptors.request.use(config => {
  const token = getToken();
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});


export async function getUser() {
  const response = await userAPI.get('/users/me');
  if (response.status !== 200) {
    throw new Error('Failed to fetch user');
  }
  return response.data.data;
}