from django.urls import path

from .views import (
    AboutView,
    CartView,
    CategoryDetailView,
    CategoryListView,
    HomeView,
    ManufacturerDetailView,
    ManufacturerListView,
    ProductDetailView,
    ProductListView,
    PromotionDetailView,
    PromotionListView,
    ReviewListView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('manufacturers/', ManufacturerListView.as_view(), name='manufacturer_list'),
    path('manufacturers/<int:pk>/', ManufacturerDetailView.as_view(), name='manufacturer_detail'),
    path('promotions/', PromotionListView.as_view(), name='promotion_list'),
    path('promotions/<int:pk>/', PromotionDetailView.as_view(), name='promotion_detail'),
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('cart/', CartView.as_view(), name='cart'),
]
