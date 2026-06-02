from rest_framework import permissions, viewsets
from rest_framework.filters import SearchFilter

from .models import Category, Customer, Manufacturer, Order, OrderItem, Product, Promotion, Review
from .serializers import (
    CategorySerializer,
    CustomerSerializer,
    ManufacturerSerializer,
    OrderItemSerializer,
    OrderSerializer,
    ProductSerializer,
    PromotionSerializer,
    ReviewSerializer,
)


class ReadOnlyOrAuthenticated(permissions.BasePermission):
    """Allow anyone to read data, but require login for writes."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class BakeryModelViewSet(viewsets.ModelViewSet):
    permission_classes = (ReadOnlyOrAuthenticated,)
    filter_backends = (SearchFilter,)


class CategoryViewSet(BakeryModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    search_fields = ('name', 'description')


class ManufacturerViewSet(BakeryModelViewSet):
    queryset = Manufacturer.objects.all().order_by('id')
    serializer_class = ManufacturerSerializer
    search_fields = ('name', 'description', 'address', 'phone')


class ProductViewSet(BakeryModelViewSet):
    queryset = Product.objects.select_related('category', 'manufacturer').all().order_by('id')
    serializer_class = ProductSerializer
    search_fields = (
        'name',
        'composition',
        'description',
        'short_description',
        'category__name',
        'manufacturer__name',
    )


class CustomerViewSet(BakeryModelViewSet):
    queryset = Customer.objects.all().order_by('id')
    serializer_class = CustomerSerializer
    search_fields = ('first_name', 'last_name', 'phone', 'email', 'address')


class OrderViewSet(BakeryModelViewSet):
    queryset = Order.objects.select_related('user', 'customer').all().order_by('id')
    serializer_class = OrderSerializer
    search_fields = (
        'status',
        'user__username',
        'customer__first_name',
        'customer__last_name',
        'customer__phone',
        'customer__email',
    )


class OrderItemViewSet(BakeryModelViewSet):
    queryset = OrderItem.objects.select_related('order', 'product').all().order_by('id')
    serializer_class = OrderItemSerializer
    search_fields = ('product__name', 'order__status')


class ReviewViewSet(BakeryModelViewSet):
    queryset = Review.objects.select_related('product').all().order_by('id')
    serializer_class = ReviewSerializer
    search_fields = ('customer_name', 'text', 'product__name')


class PromotionViewSet(BakeryModelViewSet):
    queryset = Promotion.objects.all().order_by('id')
    serializer_class = PromotionSerializer
    search_fields = ('title', 'description')
