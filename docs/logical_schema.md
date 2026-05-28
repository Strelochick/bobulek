# Логическая схема БД (магазин хлебобулочных изделий)

Сущности и связи:

1. Category (Категория)
Атрибуты: id, name, description, image
Связи: Category 1:N Product

2. Manufacturer (Производитель)
Атрибуты: id, name, description, address, phone, logo
Связи: Manufacturer 1:N Product

3. Product (Товар)
Атрибуты: id, name, category_id, price, weight, composition, description, short_description, image, is_available, manufacturer_id, created_at
Связи: Product N:1 Category, Product N:1 Manufacturer, Product 1:N Review, Product 1:N OrderItem

4. Customer (Покупатель)
Атрибуты: id, first_name, last_name, phone, email, address
Связи: Customer 1:N Order

5. Order (Заказ)
Атрибуты: id, customer_id, created_at, status, total_price
Связи: Order N:1 Customer, Order 1:N OrderItem

6. OrderItem (Позиция заказа)
Атрибуты: id, order_id, product_id, quantity, price
Связи: OrderItem N:1 Order, OrderItem N:1 Product

7. Review (Отзыв)
Атрибуты: id, product_id, customer_name, rating, text, created_at
Связи: Review N:1 Product

8. Promotion (Акция)
Атрибуты: id, title, description, discount_percent, start_date, end_date, image
Связи: самостоятельная сущность (в текущей версии без FK)

Текстовая ER-модель:
Category --< Product >-- Manufacturer
Product --< Review
Customer --< Order --< OrderItem >-- Product
Promotion (отдельно)
