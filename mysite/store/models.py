from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

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

TYPE_CHOICES = (
    ('QR code', 'QR code'),
    ('cash', 'cash'),
    ('by card', 'by card')
)

DELIVERY_CHOICES = (
('Экспресс', 'Экспресс'),
('Стандарт', 'Стандарт'),
('Эконом', 'Эконом')
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


class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


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


class Address(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=100)
    phone = PhoneNumberField()

    def __str__(self):
        return f'{self.user}, {self.city}, {self.street}, {self.phone}'


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_type = models.CharField(choices=TYPE_CHOICES, default='cash')

    def __str__(self):
        return f'{self.order}, {self.payment_type}'

class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    tracking_number = models.PositiveIntegerField()
    delivery_type = models.CharField(choices=DELIVERY_CHOICES, default='Эконом')

    def __str__(self):
        return f'{self.order}, {self.delivery_type}'


class ReturnRequest(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.order}, {self.reason}'


class PromoCode(models.Model):
    code = models.CharField(max_length=15, unique=True)
    discount_percent = models.PositiveIntegerField()
    expires_at = models.DateTimeField()

    def __str__(self):
        return f'{self.code}, {self.discount_percent}'

class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}, {self.product}'


class Notification(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}, {self.message}'


class Chat(models.Model):
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyer')
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller')

    def __str__(self):
        return f'{self.buyer}, {self.seller}'


class ChatMessage(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    image =models.ImageField(upload_to='image')
    video = models.FileField(upload_to='video', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}, {self.chat}, {self.message}'


class SellerPayout(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    status_payment = models.CharField(choices=STATUS_CHOICES, default='pending')
    paid_date = models.DateField()

    def __str__(self):
        return f'{self.seller}, {self.amount}, {self.status_payment}'


class Article(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


