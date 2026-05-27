from django.views.generic import DetailView, ListView, TemplateView

from .models import Category, Manufacturer, Product, Promotion, Review


class HomeView(TemplateView):
    template_name = 'bakery/home.html'


class AboutView(TemplateView):
    template_name = 'bakery/about.html'


class CartView(TemplateView):
    template_name = 'bakery/cart.html'


class ProductListView(ListView):
    model = Product
    template_name = 'bakery/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'bakery/product_detail.html'
    context_object_name = 'product'


class CategoryListView(ListView):
    model = Category
    template_name = 'bakery/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'bakery/category_detail.html'
    context_object_name = 'category'


class ManufacturerListView(ListView):
    model = Manufacturer
    template_name = 'bakery/manufacturer_list.html'
    context_object_name = 'manufacturers'


class ManufacturerDetailView(DetailView):
    model = Manufacturer
    template_name = 'bakery/manufacturer_detail.html'
    context_object_name = 'manufacturer'


class PromotionListView(ListView):
    model = Promotion
    template_name = 'bakery/promotion_list.html'
    context_object_name = 'promotions'


class PromotionDetailView(DetailView):
    model = Promotion
    template_name = 'bakery/promotion_detail.html'
    context_object_name = 'promotion'


class ReviewListView(ListView):
    model = Review
    template_name = 'bakery/review_list.html'
    context_object_name = 'reviews'
