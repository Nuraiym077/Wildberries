from django_filters import FilterSet
from .models import Product, Category, Order, Review

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'subcategory':['exact'],
            'price':['gt','lt']
        }

class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'category_name':['exact']
        }

class OrderFilter(FilterSet):
    class Meta:
        model = Order
        fields = {
            'user':['exact'],
            'total_price':['gt','lt']
        }

class ReviewFilter(FilterSet):
    class Meta:
       model = Review
       fields = {
           'product':['exact'],
           'rating':['exact']
       }
