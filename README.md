# IzvestNick

Готовый стартовый набор под твой запрос:
- веб-интерфейс входа/регистрации/чатов
- backend на FastAPI
- регистрация по телефону
- вход по телефону и паролю
- имя/фамилия после регистрации
- профиль, линк, фото профиля
- direct chats
- сообщения, ответы, пересылка-заготовка, удаление
- WebSocket realtime

## Запуск backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Что ещё нужно сделать до production

- PostgreSQL вместо SQLite
- Alembic миграции
- HTTPS/TLS 1.3 на сервере
- ротация refresh token
- WebSocket auth
- E2EE payload вместо открытого body
- WebRTC signaling для голосовых вызовов
- S3 для хранения медиа
- rate limiting и audit log

## Важно

В этом наборе нет механик сокрытия трафика от DPI и нет функций обхода сетевой фильтрации. Здесь заложена обычная безопасная архитектура: TLS, Argon2, JWT, WebSocket и база под дальнейшее E2EE.


## Быстрый тест в браузере

После запуска backend открой:

- `http://127.0.0.1:8000/app`

Там есть простой веб-клиент для:

- регистрации
- заполнения имени и фамилии
- логина
- создания личного чата по `user_id`
- отправки и чтения сообщений

## Деплой на Render

В репозитории уже есть `render.yaml`, поэтому можно развернуть приложение как Blueprint или как обычный Web Service.

### Минимальный вариант

- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

После деплоя:

- API: `https://<your-service>.onrender.com/docs`
- Веб-клиент: `https://<your-service>.onrender.com/app`
