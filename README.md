# Coursework web application "To Do" 

### Используемые технологии
`Flask` `SQLAlchemy` `Gunicorn` `Svelte` `TypeScript` `Nginx` `Docker` `jwt` 
___

### Описание проекта
Курсовая работа по теме "Разработка клиент-серверного фуллстек-приложения для управления списком дел"
Реализована двухуровневая клиент-серверная архитектура. Бизнес логика и база данных на одном сервере.  
Реализована минимально рабочая логика приложения. Спроектирован REST API

### Ключевые решения
– *Работа с бд через ORM*  
– *Авторизация через jwt token*  
– *Разделение бизнес логики и уровня бд*  
– *Использование TypeScript для клиентской части*  
– *Асинхронные запросы к серверу через axios*  
– *Контейнеризация через docker-compose*
___

### Диаграмма компонентов
![image](https://github.com/NikitaBalakhontsev/Coursework_webApp_todo/assets/87572909/da19f2c5-8173-4872-aff7-6298d73f2b31)


### Er диаграмма базы данных
Реализованы 4 базовые сущности: пользователь, категория, задача, тег  
![image](https://github.com/NikitaBalakhontsev/Coursework_webApp_todo/assets/87572909/bf28d903-ccd9-45fa-81f9-8184950bb360)
___

### Пример работы приложения
![image](https://github.com/NikitaBalakhontsev/Coursework_webApp_todo/assets/87572909/b633824c-a5b0-4b1c-a249-5a806a2006d0)

### Запуск из контейнера  
![image](https://github.com/NikitaBalakhontsev/Coursework_webApp_todo/assets/87572909/75ad92dd-d241-4998-ac82-6e152050f59e)




