from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

ROLE_CHOICES = (
    ('buyer', 'buyer'),
    ('seller', 'seller'),
    ('admin', 'admin')
)

STATUS_CHOICES = (
    ('pending', 'pending'),
    ('paid', 'paid'),
    ('shipped', 'shipped'),
    ('canceled', 'canceled'),
    ('delivered', 'delivered')
)

class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    role = models.CharField(choices=ROLE_CHOICES, default='buyer')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=25, unique=True)
    category_image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_category_name

class Product(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f'{self.product}, {self.image}'



class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField()
    status = models.CharField(choices=STATUS_CHOICES, default='pending')
    created_date = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.order}, {self.product}, {self.quantity}, {self.price}'


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.product}, {self.rating}, {self.comment}'



