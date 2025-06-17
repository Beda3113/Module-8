# 📄 Руководство по использованию программы: Доска объявлений
## 🧩 Общее описание
### Это веб-приложение реализует доску объявлений с возможностью:

- Создания объявления
- Поиска объявлений
- Просмотра, удаления и редактирования конкретного объявления

### Приложение состоит из двух частей:

- Backend (бэкенд) — Flask API для обработки данных
- Frontend (фронтенд) — интерфейс на HTML/CSS/JS, подключённый через FastAPI
### 🗂 Структура проекта
```
FLASK/
├── docker-compose.yml         # Конфигурация для запуска backend и frontend в Docker
├── backend/
│   ├── app.py                 # Основной код Flask API
│   ├── requirements.txt       # Зависимости Flask (flask, flask-cors)
│   └── Dockerfile             # Файл сборки Docker для backend
└── frontend/
    ├── main.py                # FastAPI сервер для фронтенда
    ├── requirements.txt       # Зависимости FastAPI (fastapi, uvicorn, jinja2)
    ├── templates/
    │   └── index.html         # Основная страница сайта
    └── static/
        └── style.css          # Стили сайта
```
##  Запуск приложения
Через Docker
```
docker-compose up -d
```
- Backend будет доступен по адресу: http://localhost:8002
- Фронтенд: http://localhost:8001


