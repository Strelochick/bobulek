from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import RegistrationForm
from .models import Category, Customer, Manufacturer, Order, OrderItem, Product, Promotion, Review


CART_SESSION_KEY = 'cart'


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class StaffOrOrderOwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        order = self.get_object()
        return self.request.user.is_staff or order.user_id == self.request.user.id


def _get_cart(session):
    return session.setdefault(CART_SESSION_KEY, {})


def _get_cart_products(cart):
    product_ids = [int(product_id) for product_id in cart.keys()]
    products = Product.objects.filter(id__in=product_ids, is_available=True)
    return {str(product.id): product for product in products}


def _parse_quantity(value, default=1):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


class HomeView(TemplateView):
    template_name = 'bakery/home.html'


class AboutView(TemplateView):
    template_name = 'bakery/about.html'


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'bakery/registration.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Регистрация выполнена. Вы вошли в аккаунт.')
        return response


class CartView(TemplateView):
    template_name = 'bakery/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = _get_cart(self.request.session)
        products = _get_cart_products(cart)
        items = []
        total_price = Decimal('0')

        for product_id, quantity in cart.items():
            product = products.get(product_id)
            if not product:
                continue
            line_total = product.price * quantity
            total_price += line_total
            items.append({
                'product': product,
                'quantity': quantity,
                'line_total': line_total,
            })

        context['cart_items'] = items
        context['total_price'] = total_price
        return context


class AddToCartView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, is_available=True)
        quantity = _parse_quantity(request.POST.get('quantity'), default=1)
        quantity = max(1, min(quantity, 99))
        cart = _get_cart(request.session)
        product_key = str(product.pk)
        cart[product_key] = cart.get(product_key, 0) + quantity
        request.session.modified = True
        messages.success(request, f'Товар "{product.name}" добавлен в корзину.')
        return redirect(request.POST.get('next') or 'cart')


class UpdateCartItemView(View):
    def post(self, request, pk):
        cart = _get_cart(request.session)
        product_key = str(pk)
        quantity = _parse_quantity(request.POST.get('quantity'), default=1)

        if quantity <= 0:
            cart.pop(product_key, None)
            messages.success(request, 'Товар удален из корзины.')
        else:
            cart[product_key] = min(quantity, 99)
            messages.success(request, 'Количество товара обновлено.')

        request.session.modified = True
        return redirect('cart')


class RemoveFromCartView(View):
    def post(self, request, pk):
        cart = _get_cart(request.session)
        cart.pop(str(pk), None)
        request.session.modified = True
        messages.success(request, 'Товар удален из корзины.')
        return redirect('cart')


class CreateOrderView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def post(self, request):
        cart = _get_cart(request.session)
        products = _get_cart_products(cart)

        if not cart or not products:
            messages.warning(request, 'Нельзя создать заказ из пустой корзины.')
            return redirect('cart')

        with transaction.atomic():
            total_price = sum(
                products[product_id].price * quantity
                for product_id, quantity in cart.items()
                if product_id in products
            )
            order = Order.objects.create(user=request.user, total_price=total_price)
            order_items = [
                OrderItem(
                    order=order,
                    product=product,
                    quantity=cart[str(product.pk)],
                    price=product.price,
                )
                for product in products.values()
            ]
            OrderItem.objects.bulk_create(order_items)

        request.session[CART_SESSION_KEY] = {}
        messages.success(request, f'Заказ #{order.pk} создан и привязан к пользователю {request.user.username}.')
        return redirect('order_detail', pk=order.pk)


class ProductListView(ListView):
    model = Product
    template_name = 'bakery/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'bakery/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(StaffRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'category', 'price', 'weight', 'composition', 'description', 'short_description', 'image', 'is_available', 'manufacturer']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('product_list')


class ProductUpdateView(StaffRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'category', 'price', 'weight', 'composition', 'description', 'short_description', 'image', 'is_available', 'manufacturer']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('product_list')


class ProductDeleteView(StaffRequiredMixin, DeleteView):
    model = Product
    template_name = 'bakery/confirm_delete.html'
    success_url = reverse_lazy('product_list')


class CategoryListView(ListView):
    model = Category
    template_name = 'bakery/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'bakery/category_detail.html'
    context_object_name = 'category'


class CategoryCreateView(StaffRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'description', 'image']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(StaffRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'description', 'image']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(StaffRequiredMixin, DeleteView):
    model = Category
    template_name = 'bakery/confirm_delete.html'
    success_url = reverse_lazy('category_list')


class ManufacturerListView(ListView):
    model = Manufacturer
    template_name = 'bakery/manufacturer_list.html'
    context_object_name = 'manufacturers'


class ManufacturerDetailView(DetailView):
    model = Manufacturer
    template_name = 'bakery/manufacturer_detail.html'
    context_object_name = 'manufacturer'


class ManufacturerCreateView(StaffRequiredMixin, CreateView):
    model = Manufacturer
    fields = ['name', 'description', 'address', 'phone', 'logo']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('manufacturer_list')


class ManufacturerUpdateView(StaffRequiredMixin, UpdateView):
    model = Manufacturer
    fields = ['name', 'description', 'address', 'phone', 'logo']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('manufacturer_list')


class ManufacturerDeleteView(StaffRequiredMixin, DeleteView):
    model = Manufacturer
    template_name = 'bakery/confirm_delete.html'
    success_url = reverse_lazy('manufacturer_list')


class PromotionListView(ListView):
    model = Promotion
    template_name = 'bakery/promotion_list.html'
    context_object_name = 'promotions'


class PromotionDetailView(DetailView):
    model = Promotion
    template_name = 'bakery/promotion_detail.html'
    context_object_name = 'promotion'


class PromotionCreateView(StaffRequiredMixin, CreateView):
    model = Promotion
    fields = ['title', 'description', 'discount_percent', 'start_date', 'end_date', 'image']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('promotion_list')


class PromotionUpdateView(StaffRequiredMixin, UpdateView):
    model = Promotion
    fields = ['title', 'description', 'discount_percent', 'start_date', 'end_date', 'image']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('promotion_list')


class PromotionDeleteView(StaffRequiredMixin, DeleteView):
    model = Promotion
    template_name = 'bakery/confirm_delete.html'
    success_url = reverse_lazy('promotion_list')


class ReviewListView(ListView):
    model = Review
    template_name = 'bakery/review_list.html'
    context_object_name = 'reviews'


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['product', 'customer_name', 'rating', 'text']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('review_list')


class ReviewUpdateView(StaffRequiredMixin, UpdateView):
    model = Review
    fields = ['product', 'customer_name', 'rating', 'text']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('review_list')


class ReviewDeleteView(StaffRequiredMixin, DeleteView):
    model = Review
    template_name = 'bakery/confirm_delete.html'
    success_url = reverse_lazy('review_list') 


class CustomerListView(StaffRequiredMixin, ListView):
    model = Customer
    template_name = 'bakery/customer_list.html'
    context_object_name = 'customers'


class CustomerDetailView(StaffRequiredMixin, DetailView):
    model = Customer
    template_name = 'bakery/customer_detail.html'
    context_object_name = 'customer'


class CustomerCreateView(StaffRequiredMixin, CreateView):
    model = Customer
    fields = ['first_name', 'last_name', 'phone', 'email', 'address']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('customer_list')


class CustomerUpdateView(StaffRequiredMixin, UpdateView):
    model = Customer
    fields = ['first_name', 'last_name', 'phone', 'email', 'address']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('customer_list')


class CustomerDeleteView(StaffRequiredMixin, DeleteView):
    model = Customer
    template_name = 'bakery/confirm_delete.html'
    success_url = reverse_lazy('customer_list')


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'bakery/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('user', 'customer')
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)


class OrderDetailView(StaffOrOrderOwnerRequiredMixin, DetailView):
    model = Order
    template_name = 'bakery/order_detail.html'
    context_object_name = 'order'


class OrderCreateView(StaffRequiredMixin, CreateView):
    model = Order
    fields = ['user', 'customer', 'status', 'total_price']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('order_list')


class OrderUpdateView(StaffRequiredMixin, UpdateView):
    model = Order
    fields = ['user', 'customer', 'status', 'total_price']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('order_list')


class OrderDeleteView(StaffRequiredMixin, DeleteView):
    model = Order
    template_name = 'bakery/confirm_delete.html'
    success_url = reverse_lazy('order_list')


class OrderItemListView(StaffRequiredMixin, ListView):
    model = OrderItem
    template_name = 'bakery/orderitem_list.html'
    context_object_name = 'order_items'


class OrderItemDetailView(StaffRequiredMixin, DetailView):
    model = OrderItem
    template_name = 'bakery/orderitem_detail.html'
    context_object_name = 'order_item'


class OrderItemCreateView(StaffRequiredMixin, CreateView):
    model = OrderItem
    fields = ['order', 'product', 'quantity', 'price']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('orderitem_list')


class OrderItemUpdateView(StaffRequiredMixin, UpdateView):
    model = OrderItem
    fields = ['order', 'product', 'quantity', 'price']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('orderitem_list')


class OrderItemDeleteView(StaffRequiredMixin, DeleteView):
    model = OrderItem
    template_name = 'bakery/confirm_delete.html'
    success_url = reverse_lazy('orderitem_list')
