from decimal import Decimal

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from .models import Category, Customer, Manufacturer, Order, OrderItem, Product, Promotion, Review
from .views import CART_SESSION_KEY
from . import views


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
        self.client.post(reverse('cart_add', args=[self.product.pk]), {'quantity': 3})

        response = self.client.post(reverse('cart_create_order'))

        order = Order.objects.get()
        self.assertRedirects(response, reverse('order_detail', args=[order.pk]))
        self.assertEqual(order.user, user)
        self.assertEqual(order.total_price, Decimal('360.00'))
        self.assertEqual(order.items.get().quantity, 3)
        self.assertEqual(self.client.session[CART_SESSION_KEY], {})

    def test_regular_user_sees_only_own_orders(self):
        buyer = User.objects.create_user(username='buyer', password='test-pass-123')
        other_user = User.objects.create_user(username='other', password='test-pass-123')
        own_order = Order.objects.create(user=buyer, total_price=Decimal('120.00'))
        other_order = Order.objects.create(user=other_user, total_price=Decimal('240.00'))
        self.client.force_login(buyer)

        list_response = self.client.get(reverse('order_list'))
        detail_response = self.client.get(reverse('order_detail', args=[own_order.pk]))
        forbidden_response = self.client.get(reverse('order_detail', args=[other_order.pk]))

        self.assertContains(list_response, f'>{own_order.pk}<')
        self.assertNotContains(list_response, f'>{other_order.pk}<')
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(forbidden_response.status_code, 403)

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


class GenericCrudTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username='manager',
            password='test-pass-123',
            is_staff=True,
        )
        self.client.force_login(self.staff)
        self.category = Category.objects.create(
            name='Булочки',
            description='Свежая выпечка',
            image='categories/test.svg',
        )
        self.manufacturer = Manufacturer.objects.create(
            name='Пекарня',
            description='Локальное производство',
            address='Москва',
            phone='+79990000000',
            logo='manufacturers/test.svg',
        )
        self.product = Product.objects.create(
            name='Круассан',
            category=self.category,
            price=Decimal('120.00'),
            weight=90,
            composition='Мука, масло',
            description='Слоеный круассан',
            short_description='Свежий круассан',
            image='products/test.svg',
            manufacturer=self.manufacturer,
        )
        self.customer = Customer.objects.create(
            first_name='Иван',
            last_name='Петров',
            phone='+79990000001',
            email='ivan@example.com',
            address='Москва',
        )
        self.order = Order.objects.create(
            user=self.staff,
            customer=self.customer,
            status='new',
            total_price=Decimal('120.00'),
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=Decimal('120.00'),
        )
        self.review = Review.objects.create(
            product=self.product,
            customer_name='Иван',
            rating=5,
            text='Отлично',
        )
        self.promotion = Promotion.objects.create(
            title='Скидка недели',
            description='Скидка на выпечку',
            discount_percent=10,
            start_date='2026-06-01',
            end_date='2026-06-30',
            image='promotions/test.svg',
        )

    def test_crud_views_are_django_generics(self):
        crud_classes = [
            (views.ProductCreateView, CreateView),
            (views.ProductUpdateView, UpdateView),
            (views.ProductDeleteView, DeleteView),
            (views.CategoryCreateView, CreateView),
            (views.CategoryUpdateView, UpdateView),
            (views.CategoryDeleteView, DeleteView),
            (views.ManufacturerCreateView, CreateView),
            (views.ManufacturerUpdateView, UpdateView),
            (views.ManufacturerDeleteView, DeleteView),
            (views.PromotionCreateView, CreateView),
            (views.PromotionUpdateView, UpdateView),
            (views.PromotionDeleteView, DeleteView),
            (views.ReviewCreateView, CreateView),
            (views.ReviewUpdateView, UpdateView),
            (views.ReviewDeleteView, DeleteView),
            (views.CustomerCreateView, CreateView),
            (views.CustomerUpdateView, UpdateView),
            (views.CustomerDeleteView, DeleteView),
            (views.OrderCreateView, CreateView),
            (views.OrderUpdateView, UpdateView),
            (views.OrderDeleteView, DeleteView),
            (views.OrderItemCreateView, CreateView),
            (views.OrderItemUpdateView, UpdateView),
            (views.OrderItemDeleteView, DeleteView),
        ]

        for view_class, generic_class in crud_classes:
            with self.subTest(view=view_class.__name__):
                self.assertTrue(issubclass(view_class, generic_class))

    def test_staff_crud_pages_are_available(self):
        pages = [
            reverse('product_create'),
            reverse('product_update', args=[self.product.pk]),
            reverse('product_delete', args=[self.product.pk]),
            reverse('category_create'),
            reverse('category_update', args=[self.category.pk]),
            reverse('category_delete', args=[self.category.pk]),
            reverse('manufacturer_create'),
            reverse('manufacturer_update', args=[self.manufacturer.pk]),
            reverse('manufacturer_delete', args=[self.manufacturer.pk]),
            reverse('promotion_create'),
            reverse('promotion_update', args=[self.promotion.pk]),
            reverse('promotion_delete', args=[self.promotion.pk]),
            reverse('review_update', args=[self.review.pk]),
            reverse('review_delete', args=[self.review.pk]),
            reverse('customer_create'),
            reverse('customer_update', args=[self.customer.pk]),
            reverse('customer_delete', args=[self.customer.pk]),
            reverse('order_create'),
            reverse('order_update', args=[self.order.pk]),
            reverse('order_delete', args=[self.order.pk]),
            reverse('orderitem_create'),
            reverse('orderitem_update', args=[self.order_item.pk]),
            reverse('orderitem_delete', args=[self.order_item.pk]),
        ]

        for url in pages:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_create_update_delete_redirect_to_list_pages(self):
        image = SimpleUploadedFile(
            'cake.gif',
            b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00\xff\xff\xff,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;',
            content_type='image/gif',
        )
        create_response = self.client.post(reverse('category_create'), {
            'name': 'Торты',
            'description': 'Праздничные торты',
            'image': image,
        })
        self.assertRedirects(create_response, reverse('category_list'))

        update_response = self.client.post(reverse('manufacturer_update', args=[self.manufacturer.pk]), {
            'name': 'Новая пекарня',
            'description': self.manufacturer.description,
            'address': self.manufacturer.address,
            'phone': self.manufacturer.phone,
        })
        self.assertRedirects(update_response, reverse('manufacturer_list'))

        delete_response = self.client.post(reverse('review_delete', args=[self.review.pk]))
        self.assertRedirects(delete_response, reverse('review_list'))
