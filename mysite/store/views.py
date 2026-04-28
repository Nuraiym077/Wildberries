from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import generics, viewsets, status
from .serializer import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .permissions import ReadOnlyOrSeller, IsProductOwner
from .permissions import IsCustomer, IsOrderOwner
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter, CategoryFilter, OrderFilter, ReviewFilter
from rest_framework.filters import  SearchFilter

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view

User = get_user_model()

@api_view(['GET'])
def search_user(request):
    email = request.query_params.get('email')
    try:
        user = User.objects.get(email=email)
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })
    except User.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

class ActivateStubView(APIView):
    def get(self, request):
        return Response({"status": "ok"})

    def post(self, request):
        return Response({"status": "ok"})



class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)



class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter
    filter_backends = [DjangoFilterBackend,SearchFilter]
    search_fields = ['category_name']


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class SubCategoryListAPIView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class SubCategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer



class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [ReadOnlyOrSeller, IsProductOwner]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filterset_class = ReviewFilter



class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsCustomer, IsOrderOwner]
    filterset_class = OrderFilter

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)



class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer



class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer



class ReturnRequestListAPIView(generics.ListAPIView):
    queryset = ReturnRequest.objects.all()
    serializer_class = ReturnRequestSerializer

    def get_queryset(self):
        return ReturnRequest.objects.filter(order__user=self.request.user)


class ReturnRequestDetailAPIView(generics.RetrieveAPIView):
    queryset = ReturnRequest.objects.all()
    serializer_class = ReturnRequestSerializer

    def get_queryset(self):
        return ReturnRequest.objects.filter(order__user=self.request.user)



class PromoCodeListAPIView(generics.ListAPIView):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer


class PromoCodeDetailAPIView(generics.RetrieveAPIView):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer



class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationDetailAPIView(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)



class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(buyer=user) | Chat.objects.filter(seller=user)


class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        chat_id = self.request.query_params.get('chat')
        if chat_id:
            # Показываем все сообщения этого чата (и мои, и чужие)
            return ChatMessage.objects.filter(chat_id=chat_id)
        return ChatMessage.objects.none()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)



class SellerPayoutListAPIView(generics.ListAPIView):
    queryset = SellerPayout.objects.all()
    serializer_class = SellerPayoutSerializer

    def get_queryset(self):
        return SellerPayout.objects.filter(seller=self.request.user)


class SellerPayoutDetailAPIView(generics.RetrieveAPIView):
    queryset = SellerPayout.objects.all()
    serializer_class = SellerPayoutSerializer

    def get_queryset(self):
        return SellerPayout.objects.filter(seller=self.request.user)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes  = [IsAuthenticated]

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
