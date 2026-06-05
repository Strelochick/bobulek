# Отчет. Настройка шаблонов и статических файлов проекта

## Цель работы

Настроить общую структуру шаблонов Django-проекта, вынести шаблоны из приложения в отдельный каталог проекта, подключить базовые статические файлы и минимизировать повторение HTML-кода за счет наследования и подключаемых элементов.

## Структура шаблонов

Шаблоны вынесены из приложения `bakery` в корневой каталог проекта:

```text
bobulek/
├── templates/
│   └── bakery/
│       ├── base.html
│       ├── home.html
│       ├── product_list.html
│       ├── product_detail.html
│       ├── category_list.html
│       ├── category_detail.html
│       ├── form.html
│       ├── confirm_delete.html
│       └── includes/
│           ├── breadcrumbs.html
│           ├── quick_actions.html
│           ├── page_header.html
│           ├── entity_image.html
│           └── detail_actions.html
```

В `bakery_project/settings.py` добавлен путь к общему каталогу шаблонов:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        ...
    },
]
```

Теперь шаблоны находятся отдельно от основного приложения, а приложение `bakery` содержит только Python-код, миграции, формы, модели, представления и маршруты.

## Базовый шаблон

Базовый шаблон реализован в файле:

```text
templates/bakery/base.html
```

Он содержит общую HTML-структуру сайта:

- подключение `meta`, `title`, favicon и CSS;
- шапку сайта с навигацией;
- блок системных сообщений;
- основной контейнер страницы;
- подвал сайта;
- подключение общего JavaScript-файла;
- блоки `title`, `meta_description`, `extra_head`, `top_elements`, `content`, `extra_scripts`.

Все основные страницы проекта наследуются от базового шаблона через:

```django
{% extends 'bakery/base.html' %}
```

## Подключаемые элементы шаблона

Созданы и используются подключаемые элементы в каталоге:

```text
templates/bakery/includes/
```

Минимум два подключаемых элемента выполнены. В проекте используется пять элементов:

- `breadcrumbs.html` - хлебные крошки;
- `quick_actions.html` - быстрые действия пользователя;
- `page_header.html` - единый заголовок страниц списков;
- `entity_image.html` - единый вывод изображения с placeholder;
- `detail_actions.html` - кнопки действий на страницах деталей.

Пример подключения:

```django
{% include 'bakery/includes/page_header.html' with title='Товары' create_url=product_create_url create_label='Добавить товар' %}
```

## Статические файлы

Базовые статические файлы проекта находятся в общем каталоге:

```text
static/
├── core/
│   ├── css/
│   │   └── global.css
│   ├── js/
│   │   └── global.js
│   └── img/
│       └── favicon.svg
└── bakery/
    ├── css/
    │   └── style.css
    └── img/
        ├── placeholder-category.svg
        ├── placeholder-manufacturer.svg
        ├── placeholder-product.svg
        └── placeholder-promotion.svg
```

В `settings.py` настроено подключение общего каталога статики:

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

В базовом шаблоне подключаются общие стили и скрипты:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'core/css/global.css' %}">
<link rel="stylesheet" href="{% static 'bakery/css/style.css' %}">
<script src="{% static 'core/js/global.js' %}"></script>
```

## Минимизация повторения кода

Страницы товаров, категорий, производителей, заказов, покупателей, акций, отзывов, корзины, авторизации и регистрации переведены на наследование от `base.html`.

Повторяющиеся элементы вынесены в `includes`, поэтому в страницах не дублируются:

- шапка и навигация;
- подвал;
- подключение CSS и JavaScript;
- хлебные крошки;
- блок быстрых действий;
- заголовки списков;
- кнопки изменения, удаления и возврата;
- логика отображения изображений и placeholder.

## Проверка

После переноса шаблонов выполнены проверки:

```bash
python manage.py check
```

Результат:

```text
System check identified no issues (0 silenced).
```

Также выполнены тесты проекта:

```bash
python manage.py test
```

Результат:

```text
Ran 7 tests in 2.185s
OK
```

## Вывод

Шаблоны проекта вынесены в отдельный каталог `templates`, базовый шаблон реализован, подключаемые элементы созданы и используются, статические файлы подключены через общий каталог `static`. Страницы проекта используют наследование и include-шаблоны, что уменьшает дублирование HTML-кода и упрощает поддержку проекта.
