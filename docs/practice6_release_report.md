# Практика 6. Настройка release-версии и развертывание проекта в Docker

## Цель работы

Настроить production/release-структуру Django-проекта пекарни, подготовить запуск через Gunicorn, настроить nginx как reverse proxy и сервер статических файлов, а также проверить, что административная панель Django отображается корректно.

## Структура проекта

В проект добавлены файлы и каталоги для контейнерного развертывания:

```text
bobulek/
├── bakery/
├── bakery_project/
├── docker/
│   └── entrypoint.sh
├── nginx/
│   └── default.conf
├── static/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.docker
├── manage.py
└── requirements.txt
```

Назначение новых файлов:

- `Dockerfile` описывает release-образ Django-приложения на Python 3.12.
- `docker-compose.yml` запускает три сервиса: `db` с PostgreSQL, `web` с Django/Gunicorn и `nginx` для приема HTTP-запросов.
- `docker/entrypoint.sh` ожидает готовность PostgreSQL, применяет миграции, собирает статику и создает администратора.
- `nginx/default.conf` проксирует запросы к Gunicorn и отдельно отдает `/static/` и `/media/`.
- `.env.docker` содержит переменные окружения для release-запуска.
- `.dockerignore` исключает локальные и временные файлы из Docker-контекста.

## Настройка Django для release-версии

В `bakery_project/settings.py` настроены параметры, необходимые для запуска без `DEBUG`:

- `STATIC_URL = '/static/'`;
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`;
- `MEDIA_URL = '/media/'`;
- `MEDIA_ROOT = BASE_DIR / 'media'`;
- `ALLOWED_HOSTS` берется из переменной окружения;
- `CSRF_TRUSTED_ORIGINS` берется из переменной окружения;
- `SECURE_PROXY_SSL_HEADER` добавлен для корректной работы за reverse proxy.

В `requirements.txt` добавлена зависимость:

```text
gunicorn==22.0.0
```

## Настройка Gunicorn

Gunicorn запускается в контейнере `web` командой:

```bash
gunicorn bakery_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

Он принимает запросы внутри Docker-сети на порту `8000`. Внешний доступ к приложению идет через nginx.

## Настройка nginx

В `nginx/default.conf` настроен сервер на порту `80`.

Основные правила:

- `/static/` отдается из `/var/www/static/`;
- `/media/` отдается из `/var/www/media/`;
- остальные запросы проксируются в `web:8000`;
- в proxy-заголовках передаются `Host`, IP клиента и схема запроса.

Благодаря отдельной отдаче статики nginx корректно загружает CSS и JavaScript административной панели Django.

## Запуск проекта

Для запуска release-версии используются команды:

```bash
docker compose up --build
```

После запуска проект доступен по адресу:

```text
http://localhost/
```

Административная панель доступна по адресу:

```text
http://localhost/admin/
```

Данные администратора из `.env.docker`:

```text
Логин: admin
Пароль: admin12345
```

## Проверка работоспособности

Выполнены локальные проверки Django с production-переменными окружения:

```bash
DEBUG=False
SECRET_KEY=django-release-6-bakery-project-secret-key-2026-local-docker-only
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1
python manage.py check
```

Результат:

```text
System check identified no issues (0 silenced).
```

Также выполнена сборка статических файлов:

```bash
python manage.py collectstatic --noinput --clear
```

Результат:

```text
168 static files copied to staticfiles.
```

Дополнительная проверка dry-run подтвердила, что статика уже собрана:

```text
0 static files copied to staticfiles, 168 unmodified.
```

Docker CLI в текущем окружении проверки не установлен, поэтому фактический запуск `docker compose up --build` на этой машине выполнить невозможно. Конфигурация проекта подготовлена для запуска в Docker Desktop или на сервере с установленным Docker.

## Вывод

Release-структура проекта настроена. Django-приложение подготовлено к запуску через Gunicorn, nginx настроен как reverse proxy и сервер статических и медиафайлов. Административная панель Django должна отображаться корректно, так как статика собирается командой `collectstatic` в общий Docker-volume и отдается nginx по маршруту `/static/`.
