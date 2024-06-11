// src/api/category.ts
import axios from 'axios';
import { getToken } from '../stores/authStore';
import type { Category } from '../types';

const categoryAPI = axios.create({
    baseURL: 'http://127.0.0.1:8000/api'
});

categoryAPI.interceptors.request.use(config => {
  const token = getToken();
  if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

export async function fetchCategories(): Promise<Category[]> {
    const response = await categoryAPI.get('/categories');
    if (response.status === 200) {
        console.log("Categories fetched:", response.data.data);  // Debugging line
        return response.data.data as Category[];
    } else {
        throw new Error(response.data.error || 'Failed to fetch categories');
    }
}


export async function addCategory(name: string): Promise<Category> {
    const response = await categoryAPI.post('/categories', { name });
    if (response.status === 201) {
        console.log("Category added:", response.data.data);
        return response.data.data as Category;
    } else {
        throw new Error(response.data.error || 'Failed to add category');
    }
}

export async function updateCategoryName(categoryId: number, newName: string): Promise<Category> {
    const response = await categoryAPI.put(`/categories/${categoryId}`, { name: newName });
    if (response.status === 200) {
        console.log("Category updated:", response.data.data);
        return response.data.data as Category;
    } else {
        throw new Error(response.data.error || 'Failed to update category name');
    }
}

export async function deleteCategory(categoryId: number): Promise<void> {
    const response = await categoryAPI.delete(`/categories/${categoryId}`);
    if (response.status === 204) {
        console.log("Category deleted");
    } else {
        throw new Error(response.data.error || 'Failed to delete category');
    }
}






