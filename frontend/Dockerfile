# Используем образ node:20-alpine3.16 для сборки
FROM node:20-alpine3.16 as build

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем package.json и package-lock.json (если есть)
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install && \
    npm install svelte-routing && \
    npm install axios

# Копируем остальные файлы проекта
COPY . .

# Собираем проект
RUN npm run build

# Используем другой образ для сервировки статических файлов
FROM nginx:alpine

# Копируем собранные файлы из предыдущего этапа
COPY --from=build /app/dist /usr/share/nginx/html

# Копируем конфиг сервера Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Указываем порт, который будет прослушивать Nginx
EXPOSE 80

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]