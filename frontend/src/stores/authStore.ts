import { writable } from 'svelte/store';

const storedToken = localStorage.getItem('token');

export const token = writable<string | null>(storedToken);

export function setToken(newToken: string) {
  console.log('Set token');
  token.set(newToken);
  localStorage.setItem('token', newToken);
}

export function clearToken() {
  console.log('Clearing token');
  token.set(null);
  localStorage.removeItem('token');
}

export function getToken() {
  let currentToken: string | null = null;
  token.subscribe(value => currentToken = value)();
  return currentToken;
}