import django_filters
from .models import Product, Category, Order, Review

class ProductFilter(django_filters.FilterSet):
    # Настраиваем цену, чтобы названия совпадали с фронтендом (price_min/price_max)
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = {
            'category': ['exact'],      # ТЕПЕРЬ БУДЕТ РАБОТАТЬ!
            'subcategory': ['exact'],
            'seller': ['exact'],
        }

class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            'category_name': ['icontains'] # Удобнее искать по части имени
        }

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'user': ['exact'],
            'status': ['exact'], # Полезно фильтровать по статусу заказа
        }

class ReviewFilter(django_filters.FilterSet):
    class Meta:
       model = Review
       fields = {
           'product': ['exact'],
           'rating': ['exact']
       }