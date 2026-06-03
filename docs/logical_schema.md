# Логическая схема БД

Проект: интернет-магазин хлебобулочных изделий.

## Сущности

1. Category (Категория)
   - Атрибуты: id, name, description, image.
   - Связи: одна категория содержит много товаров.

2. Manufacturer (Производитель)
   - Атрибуты: id, name, description, address, phone, logo.
   - Связи: один производитель выпускает много товаров.

3. Product (Товар)
   - Атрибуты: id, name, category, price, weight, composition, description, short_description, image, is_available, manufacturer, created_at.
   - Связи: товар относится к одной категории и одному производителю; товар может входить во многие позиции заказов; товар может иметь много отзывов.

4. Customer (Покупатель)
   - Атрибуты: id, first_name, last_name, phone, email, address.
   - Связи: покупатель может иметь много заказов. При удалении покупателя заказ сохраняется, ссылка на покупателя очищается.

5. Order (Заказ)
   - Атрибуты: id, user, customer, created_at, status, total_price.
   - Связи: заказ может быть привязан к пользователю Django и покупателю; один заказ содержит много позиций заказа.

6. OrderItem (Позиция заказа)
   - Атрибуты: id, order, product, quantity, price.
   - Связи: позиция относится к одному заказу и одному товару.

7. Review (Отзыв)
   - Атрибуты: id, product, customer_name, rating, text, created_at.
   - Связи: отзыв относится к одному товару.

8. Promotion (Акция)
   - Атрибуты: id, title, description, discount_percent, start_date, end_date, image.
   - Связи: самостоятельная сущность без внешних ключей в текущей версии модели.

## Текстовая ER-модель

```text
Category 1 -- N Product
Manufacturer 1 -- N Product
Product 1 -- N Review
Product 1 -- N OrderItem
Customer 1 -- N Order
User 1 -- N Order
Order 1 -- N OrderItem
Promotion
```
