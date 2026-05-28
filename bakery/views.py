from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

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


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'category', 'price', 'weight', 'composition', 'description', 'short_description', 'image', 'is_available', 'manufacturer']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('product_list')


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'category', 'price', 'weight', 'composition', 'description', 'short_description', 'image', 'is_available', 'manufacturer']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('product_list')


class ProductDeleteView(DeleteView):
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


class CategoryCreateView(CreateView):
    model = Category
    fields = ['name', 'description', 'image']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'description', 'image']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(DeleteView):
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


class ManufacturerCreateView(CreateView):
    model = Manufacturer
    fields = ['name', 'description', 'address', 'phone', 'logo']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('manufacturer_list')


class ManufacturerUpdateView(UpdateView):
    model = Manufacturer
    fields = ['name', 'description', 'address', 'phone', 'logo']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('manufacturer_list')


class ManufacturerDeleteView(DeleteView):
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


class PromotionCreateView(CreateView):
    model = Promotion
    fields = ['title', 'description', 'discount_percent', 'start_date', 'end_date', 'image']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('promotion_list')


class PromotionUpdateView(UpdateView):
    model = Promotion
    fields = ['title', 'description', 'discount_percent', 'start_date', 'end_date', 'image']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('promotion_list')


class PromotionDeleteView(DeleteView):
    model = Promotion
    template_name = 'bakery/confirm_delete.html'
    success_url = reverse_lazy('promotion_list')


class ReviewListView(ListView):
    model = Review
    template_name = 'bakery/review_list.html'
    context_object_name = 'reviews'


class ReviewCreateView(CreateView):
    model = Review
    fields = ['product', 'customer_name', 'rating', 'text']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('review_list')


class ReviewUpdateView(UpdateView):
    model = Review
    fields = ['product', 'customer_name', 'rating', 'text']
    template_name = 'bakery/form.html'
    success_url = reverse_lazy('review_list')


class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'bakery/confirm_delete.html'
    success_url = reverse_lazy('review_list')
