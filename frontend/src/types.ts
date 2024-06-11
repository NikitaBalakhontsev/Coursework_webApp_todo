// src/types.ts
export interface Tag {
  id: number;
  description: string | null;
  color: string;
}

export interface Task {
  id: number;
  title: string;
  description: string;
  due_date: string | null;
  tags: Tag[];
  timestamp: string;
  category_id: number;
}

export interface Category {
  id: number;
  title: string;
  cards: Task[];
  // другие свойства категории, если есть
}