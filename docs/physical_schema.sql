-- Физическая схема БД PostgreSQL (по текущим моделям Django)

CREATE TABLE bakery_category (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    description TEXT NOT NULL,
    image VARCHAR(100) NOT NULL
);

CREATE TABLE bakery_manufacturer (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    logo VARCHAR(100) NOT NULL
);

CREATE TABLE bakery_customer (
    id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    email VARCHAR(254) NOT NULL,
    address VARCHAR(255) NOT NULL
);

CREATE TABLE bakery_product (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category_id BIGINT NOT NULL REFERENCES bakery_category(id) ON DELETE CASCADE,
    price NUMERIC(10,2) NOT NULL,
    weight INTEGER NOT NULL CHECK (weight >= 0),
    composition TEXT NOT NULL,
    description TEXT NOT NULL,
    short_description VARCHAR(255) NOT NULL,
    image VARCHAR(100) NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    manufacturer_id BIGINT NOT NULL REFERENCES bakery_manufacturer(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE bakery_order (
    id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES bakery_customer(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'new',
    total_price NUMERIC(10,2) NOT NULL
);

CREATE TABLE bakery_orderitem (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES bakery_order(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES bakery_product(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity >= 0),
    price NUMERIC(10,2) NOT NULL
);

CREATE TABLE bakery_review (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES bakery_product(id) ON DELETE CASCADE,
    customer_name VARCHAR(150) NOT NULL,
    rating SMALLINT NOT NULL CHECK (rating >= 0),
    text TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE bakery_promotion (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    discount_percent SMALLINT NOT NULL CHECK (discount_percent >= 0),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    image VARCHAR(100) NOT NULL
);
