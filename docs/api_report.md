# Отчет по API

## Цель

Создан REST API для CRUD-действий ко всем таблицам приложения пекарни.

## Реализация CRUD через Django REST Framework

В проект добавлен Django REST Framework и создан REST API по адресу `/api/`.

Реализованы сериализаторы и `ModelViewSet` для всех таблиц:

- `/api/categories/` - категории.
- `/api/manufacturers/` - производители.
- `/api/products/` - товары.
- `/api/customers/` - покупатели.
- `/api/orders/` - заказы.
- `/api/order-items/` - позиции заказов.
- `/api/reviews/` - отзывы.
- `/api/promotions/` - акции.

Для каждого ресурса доступны стандартные CRUD-запросы:

- `GET /api/<resource>/` - список записей.
- `GET /api/<resource>/<id>/` - одна запись.
- `POST /api/<resource>/` - создание записи.
- `PUT /api/<resource>/<id>/` - полное обновление записи.
- `PATCH /api/<resource>/<id>/` - частичное обновление записи.
- `DELETE /api/<resource>/<id>/` - удаление записи.

## Демонстрация запросов через Postman или другое ПО

Проверку можно выполнить не через браузер, а через Postman, Insomnia, Thunder Client или curl с устройства участника команды.

Для проверки с другого устройства в одной сети нужно запустить сервер так:

```bash
python manage.py runserver 0.0.0.0:8000
```

В `.env` нужно указать IP компьютера, на котором запущен Django:

```env
ALLOWED_HOSTS=127.0.0.1,localhost,<IP_компьютера_с_Django>
```

После этого в Postman на устройстве сокомандника используется адрес вида `http://<IP_компьютера_с_Django>:8000/api/products/`.

Примеры запросов:

```http
GET http://127.0.0.1:8000/api/products/
```

```http
GET http://127.0.0.1:8000/api/products/?search=хлеб&page=1&page_size=3
```

```http
POST http://127.0.0.1:8000/api/categories/
Authorization: Basic <login:password>
Content-Type: multipart/form-data

name=Новая категория
description=Описание категории
image=<файл изображения>
```

```http
PATCH http://127.0.0.1:8000/api/products/1/
Authorization: Basic <login:password>
Content-Type: application/json

{
  "is_available": false
}
```

```http
DELETE http://127.0.0.1:8000/api/reviews/1/
Authorization: Basic <login:password>
```

## Разграничение прав доступа

Для API настроены права доступа:

- чтение данных (`GET`, `HEAD`, `OPTIONS`) доступно всем пользователям;
- создание, изменение и удаление (`POST`, `PUT`, `PATCH`, `DELETE`) доступно только авторизованным пользователям.

Авторизация поддерживается через session authentication и basic authentication. Для проверки в Postman можно выбрать `Authorization -> Basic Auth` и указать логин/пароль пользователя Django.

## Поиск по данным API

Поиск реализован через параметр `search`.

Примеры:

```http
GET http://127.0.0.1:8000/api/products/?search=булочка
GET http://127.0.0.1:8000/api/customers/?search=ivan@example.com
GET http://127.0.0.1:8000/api/orders/?search=processing
```

Поиск настроен по текстовым полям моделей и связанным полям, например по названию категории, названию производителя, имени покупателя и названию товара.

## Пагинация

В API включена постраничная выдача данных. По умолчанию выводится 5 записей на страницу.

Переход между страницами:

```http
GET http://127.0.0.1:8000/api/products/?page=2
```

Изменение количества записей на странице:

```http
GET http://127.0.0.1:8000/api/products/?page=1&page_size=10
```

Ответ API содержит поля `count`, `next`, `previous` и `results`, что подтверждает работу пагинации.
