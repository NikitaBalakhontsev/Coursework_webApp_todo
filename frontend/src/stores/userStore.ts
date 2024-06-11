import { writable } from 'svelte/store';

interface User {
  id: number;
  username: string;
  email: string;
}

const storedUser = localStorage.getItem('user');
//const initialUser = storedUser ? JSON.parse(storedUser) : null;

export const user = writable<User | null>();

export function setUser(newUser: User) {
  user.set(newUser);
  localStorage.setItem('user', JSON.stringify(newUser));
}

export function clearUser() {
  user.set(null);
  localStorage.removeItem('user');
}
