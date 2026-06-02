from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField('Название', max_length=120)
    description = models.TextField('Описание')
    image = models.ImageField('Фото категории', upload_to='categories/')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField('Название', max_length=150)
    description = models.TextField('Описание')
    address = models.CharField('Адрес', max_length=255)
    phone = models.CharField('Телефон', max_length=30)
    logo = models.ImageField('Логотип', upload_to='manufacturers/')

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Название', max_length=150)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    weight = models.PositiveIntegerField('Вес', help_text='Вес в граммах')
    composition = models.TextField('Состав')
    description = models.TextField('Подробное описание')
    short_description = models.CharField('Краткое описание', max_length=255)
    image = models.ImageField('Фото товара', upload_to='products/')
    is_available = models.BooleanField('В наличии', default=True)
    manufacturer = models.ForeignKey('Manufacturer', verbose_name='Производитель', on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('Email')
    address = models.CharField('Адрес', max_length=255)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('delivery', 'Доставка'),
        ('done', 'Завершен'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='orders',
        null=True,
        blank=True,
    )
    customer = models.ForeignKey(
        'Customer',
        verbose_name='Покупатель',
        on_delete=models.SET_NULL,
        related_name='orders',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField('Дата заказа', auto_now_add=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    total_price = models.DecimalField('Итоговая сумма', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey('Order', verbose_name='Заказ', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', verbose_name='Товар', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField('Цена на момент заказа', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'


class Review(models.Model):
    product = models.ForeignKey('Product', verbose_name='Товар', on_delete=models.CASCADE, related_name='reviews')
    customer_name = models.CharField('Имя покупателя', max_length=150)
    rating = models.PositiveSmallIntegerField('Оценка')
    text = models.TextField('Текст отзыва')
    created_at = models.DateTimeField('Дата отзыва', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв {self.customer_name} ({self.rating}/5)'


class Promotion(models.Model):
    title = models.CharField('Название акции', max_length=150)
    description = models.TextField('Описание')
    discount_percent = models.PositiveSmallIntegerField('Процент скидки')
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания')
    image = models.ImageField('Фото акции', upload_to='promotions/')

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self):
        return self.title

