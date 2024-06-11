// src/api/task.ts
import axios from 'axios';
import { getToken } from '../stores/authStore';
import type { Task } from '../types';

const taskAPI = axios.create({
  baseURL: 'http://176.53.160.126:8000/api'
});

taskAPI.interceptors.request.use(config => {
  const token = getToken();
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});


export async function fetchTasks(categoryId: number): Promise<Task[]> {
    const response = await taskAPI.get(`/tasks?category_id=${categoryId}`);
    if (response.status === 200) {
        console.log("Tasks fetched:", response.data.data);  // Debugging line
        return response.data.data as Task[];
    } else {
        throw new Error(response.data.error || 'Failed to fetch tasks');
    }
  }