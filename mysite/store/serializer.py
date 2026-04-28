from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# --- 1. ПОЛЬЗОВАТЕЛИ ---

class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number', 'role']

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'username', 'password', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

# --- 2. КАТЕГОРИИ ---

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_image']

class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'sub_category_name', 'category']

# --- 3. ТОВАРЫ И КАРТИНКИ ---

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'discount_price', 'image', 'avg_rating', 'category']

    def get_image(self, obj):
        # Используем .images, так как в models.py указано related_name='images'
        first_image = obj.images.first()
        if first_image and first_image.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(first_image.image.url)
            return first_image.image.url
        return None

    def get_avg_rating(self, obj):
        reviews = obj.review_set.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0.0

class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    seller = UserProfileListSerializer(read_only=True)
    avg_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'category', 'subcategory', 'product_name',
            'description', 'price', 'discount_price', 'quantity',
            'created_date', 'images', 'avg_rating', 'review_count'
        ]

    def get_avg_rating(self, obj):
        reviews = obj.review_set.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0.0

    def get_review_count(self, obj):
        return obj.review_set.count()

# --- 4. КОРЗИНА И ЗАКАЗЫ ---

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total']

    def get_total(self, obj):
        price = obj.product.discount_price or obj.product.price
        return price * obj.quantity

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True, source='cartitem_set')
    cart_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'cart_total']

    def get_cart_total(self, obj):
        return sum(
            (item.product.discount_price or item.product.price) * item.quantity
            for item in obj.cartitem_set.all()
        )

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'total_price', 'status', 'created_date']

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')
    user = UserProfileListSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total_price', 'status', 'created_date']

# --- 5. ДОПОЛНИТЕЛЬНЫЕ СЕРВИСЫ ---

class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_date']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'city', 'street', 'phone']

class PaymentSerializer(serializers.ModelSerializer):
    order = OrderListSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = ['id', 'order', 'payment_type']

class DeliverySerializer(serializers.ModelSerializer):
    order = OrderListSerializer(read_only=True)
    class Meta:
        model = Delivery
        fields = ['id', 'order', 'tracking_number', 'delivery_type']

class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product']

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserProfileListSerializer(read_only=True)
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'message', 'image', 'video', 'created_date']

class ChatSerializer(serializers.ModelSerializer):
    buyer = UserProfileListSerializer(read_only=True)
    seller = UserProfileListSerializer(read_only=True)
    messages = ChatMessageSerializer(many=True, read_only=True, source='chatmessage_set')
    class Meta:
        model = Chat
        fields = ['id', 'buyer', 'seller', 'messages']

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


# --- 6. ДОПОЛНИТЕЛЬНО (ВОЗВРАТЫ, ПРОМОКОДЫ И ВЫПЛАТЫ) ---

class ReturnRequestSerializer(serializers.ModelSerializer):
    order = OrderListSerializer(read_only=True)
    class Meta:
        model = ReturnRequest
        fields = ['id', 'order', 'reason', 'status']

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ['id', 'code', 'discount_percent', 'expires_at']

class SellerPayoutSerializer(serializers.ModelSerializer):
    seller = UserProfileListSerializer(read_only=True)
    class Meta:
        model = SellerPayout
        fields = ['id', 'seller', 'amount', 'status_payment', 'paid_date']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read']

