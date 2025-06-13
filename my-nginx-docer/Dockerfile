# Используем официальный образ Nginx на базе Alpine (легковесный)
FROM nginx:alpine

# Удаляем стандартную страницу Nginx
RUN rm -rf /usr/share/nginx/html/*

# Копируем нашу кастомную страницу
COPY index.html /usr/share/nginx/html/

# Открываем порт 80
EXPOSE 80

# Команда для запуска Nginx
CMD ["nginx", "-g", "daemon off;"]
