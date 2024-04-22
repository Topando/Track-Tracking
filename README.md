# Track Tracking
Track Tracking - это ваша статистика по прослушанным треками и форум
## Установка и запуск

### 1. Скачивание проекта
```bash
git clone https://github.com/Topando/Track-Tracking.git
```

### 2. Миграция БД
```bash
python manage.py makemigrations
python manage.py migrate
```


## Консольный функционал
### Установка зависимостей для backend
```bash
pip install -r requirements.txt
```
### Установка зависимостей для client
```bash
cd client
npm install
npm run dev
```

### Создание суперпользователя
```bash
python manage.py createsuperuser
```

### Запуск сервера backend
```bash
python backend/manage.py runserver
```

### Документация API
```
api/v1/swagger/
api/v1/redoc/
```