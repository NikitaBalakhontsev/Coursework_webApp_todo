// src/api/auth.ts
import axios from 'axios';
import { setToken, getToken, clearToken } from '../stores/authStore';

const authAPI = axios.create({
  baseURL: 'http://176.53.160.126:8000/auth'
});

authAPI.interceptors.request.use(config => {
  const token = getToken();
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});


export async function validate_token() {
  try {
    const response = await authAPI.post('/validate_token');
    if (response.status === 200) {
      console.log("user_id", response.data.data.user_id);
    } else {
      throw new Error(response.data.error);
    }
  } catch (error: any) {
    if (error.response.status === 401) {
      // Если получен код ответа 401, это означает, что токен истек
      console.log("токет истек");
      clearToken()
    } else {
      throw error; // Проброс исключения для дальнейшей обработки
    }
  }
}

export async function register(username: string, email: string, password: string) {
  const response = await authAPI.post('/authorize', { username, email, password });
  if (response.status === 201) {
    await login(email, password);
  } else {
    throw new Error(response.data.error);
  }
}


export async function login(email: string, password: string) {
  try {
    const response = await authAPI.post('/login', { email, password });
    if (response.status === 200) {
      setToken(response.data.data.token);
      // const userData = await getUser();
      // setUser(userData);
    } else {
      throw new Error(response.data.error);
    }
  } catch (error: any) {
    throw error;
  }
}

export function logout() {
  clearToken();
  // clearUser();
}
