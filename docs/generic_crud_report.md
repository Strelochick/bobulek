# Отчет: CRUD-действия через Django Generic Views

## Цель

Познакомиться с созданием действий добавления, удаления и изменения данных с помощью generic views в Django.

## Что реализовано

В приложении `bakery` CRUD-действия реализованы через классы `CreateView`, `UpdateView`, `DeleteView`, а вывод данных через `ListView` и `DetailView`.

Операции добавления, изменения и удаления доступны для 8 таблиц:

1. `Product` - товары.
2. `Category` - категории.
3. `Manufacturer` - производители.
4. `Promotion` - акции.
5. `Review` - отзывы.
6. `Customer` - покупатели.
7. `Order` - заказы.
8. `OrderItem` - позиции заказов.

Минимальное требование по 5 основным таблицам выполнено с запасом.

## Использованные generic views

В файле `bakery/views.py` для каждой сущности созданы классы:

- `ListView` - вывод списка записей;
- `DetailView` - просмотр одной записи;
- `CreateView` - добавление записи;
- `UpdateView` - изменение записи;
- `DeleteView` - удаление записи.

Для служебных действий добавления/изменения/удаления используется `StaffRequiredMixin`, поэтому управлять основными таблицами может только пользователь с правами staff.

## Страницы и маршруты

Маршруты подключены в `bakery/urls.py`.

Примеры страниц:

- `/products/`, `/products/create/`, `/products/<id>/update/`, `/products/<id>/delete/`;
- `/categories/`, `/categories/create/`, `/categories/<id>/update/`, `/categories/<id>/delete/`;
- `/manufacturers/`, `/manufacturers/create/`, `/manufacturers/<id>/update/`, `/manufacturers/<id>/delete/`;
- `/promotions/`, `/promotions/create/`, `/promotions/<id>/update/`, `/promotions/<id>/delete/`;
- `/reviews/`, `/reviews/create/`, `/reviews/<id>/update/`, `/reviews/<id>/delete/`;
- `/customers/`, `/customers/create/`, `/customers/<id>/update/`, `/customers/<id>/delete/`;
- `/orders/`, `/orders/create/`, `/orders/<id>/update/`, `/orders/<id>/delete/`;
- `/order-items/`, `/order-items/create/`, `/order-items/<id>/update/`, `/order-items/<id>/delete/`.

После успешного создания, изменения или удаления запись возвращает пользователя на соответствующую страницу списка через `success_url`.

## Шаблоны

Данные выводятся через Django templates:

- циклы `{% for %}`;
- условия `{% if %}`;
- ссылки `{% url %}`;
- переменные `{{ object.field }}`;
- фильтры дат `{{ created_at|date:'d.m.Y H:i' }}`.

Для форм используется общий шаблон `bakery/templates/bakery/form.html`.
Для удаления используется общий шаблон `bakery/templates/bakery/confirm_delete.html`.

## Административная панель

Все таблицы зарегистрированы в `bakery/admin.py`:

- `Category`;
- `Manufacturer`;
- `Product`;
- `Customer`;
- `Order`;
- `OrderItem`;
- `Review`;
- `Promotion`.

Для читаемого отображения настроены `list_display`, `list_filter` и `search_fields`.

## Схемы базы данных

Созданы и обновлены схемы:

- логическая схема: `docs/logical_schema.md`;
- физическая схема: `docs/physical_schema.sql`.

Физическая схема учитывает текущую модель `Order`: заказ может быть связан с пользователем Django (`user`) и необязательным покупателем (`customer`).
