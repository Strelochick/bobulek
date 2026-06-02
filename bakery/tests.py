from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Category, Manufacturer, Order, Product
from .views import CART_SESSION_KEY


class CartAndAuthTests(TestCase):
    def setUp(self):
        category = Category.objects.create(
            name='Булочки',
            description='Свежая выпечка',
            image='categories/test.svg',
        )
        manufacturer = Manufacturer.objects.create(
            name='Пекарня',
            description='Локальное производство',
            address='Москва',
            phone='+79990000000',
            logo='manufacturers/test.svg',
        )
        self.product = Product.objects.create(
            name='Круассан',
            category=category,
            price=Decimal('120.00'),
            weight=90,
            composition='Мука, масло',
            description='Слоеный круассан',
            short_description='Свежий круассан',
            image='products/test.svg',
            manufacturer=manufacturer,
        )

    def test_add_to_cart_stores_product_in_session(self):
        response = self.client.post(reverse('cart_add', args=[self.product.pk]), {'quantity': 2})

        self.assertRedirects(response, reverse('cart'))
        self.assertEqual(self.client.session[CART_SESSION_KEY][str(self.product.pk)], 2)

    def test_create_order_links_current_user_and_clears_cart(self):
        user = User.objects.create_user(username='buyer', password='test-pass-123')
        self.client.force_login(user)
        session = self.client.session
        session[CART_SESSION_KEY] = {str(self.product.pk): 3}
        session.save()

        response = self.client.post(reverse('cart_create_order'))

        self.assertRedirects(response, reverse('cart'))
        order = Order.objects.get()
        self.assertEqual(order.user, user)
        self.assertEqual(order.total_price, Decimal('360.00'))
        self.assertEqual(order.items.get().quantity, 3)
        self.assertEqual(self.client.session[CART_SESSION_KEY], {})

    def test_header_switches_auth_links(self):
        guest_response = self.client.get(reverse('home'))

        self.assertContains(guest_response, 'Авторизация')
        self.assertContains(guest_response, 'Регистрация')
        self.assertNotContains(guest_response, 'Выход')

        user = User.objects.create_user(username='buyer', password='test-pass-123')
        self.client.force_login(user)
        user_response = self.client.get(reverse('home'))

        self.assertContains(user_response, 'Выход')
        self.assertNotContains(user_response, 'Авторизация')
        self.assertNotContains(user_response, 'Регистрация')

