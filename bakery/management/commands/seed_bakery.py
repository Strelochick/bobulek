from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand

from bakery.models import Category, Customer, Manufacturer, Order, OrderItem, Product, Promotion, Review


class Command(BaseCommand):
    help = 'Заполняет БД тестовыми данными.'

    def handle(self, *args, **options):
        if Category.objects.exists():
            self.stdout.write(self.style.WARNING('Данные уже существуют.'))
            return

        categories = [
            Category.objects.create(name='Хлеб', description='Классический хлеб', image='categories/bread.jpg'),
            Category.objects.create(name='Булочки', description='Сладкие и сдобные булочки', image='categories/buns.jpg'),
            Category.objects.create(name='Пироги', description='Пироги с разными начинками', image='categories/pies.jpg'),
            Category.objects.create(name='Круассаны', description='Французская выпечка', image='categories/croissants.jpg'),
            Category.objects.create(name='Диетическая выпечка', description='Полезная выпечка', image='categories/fit.jpg'),
        ]

        manufacturers = [
            Manufacturer.objects.create(name='Пекарня №1', description='Локальная пекарня', address='Москва, ул. Первая, 1', phone='+79000000001', logo='manufacturers/m1.jpg'),
            Manufacturer.objects.create(name='Хлебозавод Традиция', description='Крупный поставщик', address='Москва, ул. Вторая, 2', phone='+79000000002', logo='manufacturers/m2.jpg'),
            Manufacturer.objects.create(name='Булка и Ко', description='Семейное производство', address='Москва, ул. Третья, 3', phone='+79000000003', logo='manufacturers/m3.jpg'),
        ]

        products = []
        for i in range(10):
            products.append(Product.objects.create(
                name=f'Товар {i+1}',
                category=categories[i % len(categories)],
                price=Decimal('45.00') + i * 10,
                weight=300 + i * 20,
                composition='Мука, вода, соль, дрожжи',
                description='Подробное описание хлебобулочного изделия.',
                short_description='Свежий и ароматный продукт.',
                image='products/sample.jpg',
                is_available=True,
                manufacturer=manufacturers[i % len(manufacturers)],
            ))

        customers = [
            Customer.objects.create(first_name='Иван', last_name='Иванов', phone='+79991110011', email='ivan@example.com', address='Москва'),
            Customer.objects.create(first_name='Мария', last_name='Петрова', phone='+79992220022', email='maria@example.com', address='Химки'),
            Customer.objects.create(first_name='Олег', last_name='Сидоров', phone='+79993330033', email='oleg@example.com', address='Мытищи'),
        ]

        for idx, customer in enumerate(customers, start=1):
            order = Order.objects.create(customer=customer, status='new', total_price=Decimal('320.00') + idx * 50)
            OrderItem.objects.create(order=order, product=products[idx], quantity=2, price=products[idx].price)
            OrderItem.objects.create(order=order, product=products[idx + 1], quantity=1, price=products[idx + 1].price)

        for i in range(5):
            Review.objects.create(product=products[i], customer_name=f'Покупатель {i+1}', rating=5 - (i % 2), text='Очень вкусно, рекомендую!',)

        for i in range(3):
            Promotion.objects.create(
                title=f'Акция {i+1}',
                description='Скидка на популярные позиции.',
                discount_percent=10 + i * 5,
                start_date=date.today() - timedelta(days=2),
                end_date=date.today() + timedelta(days=10 + i),
                image='promotions/promo.jpg',
            )

        self.stdout.write(self.style.SUCCESS('Тестовые данные добавлены.'))
