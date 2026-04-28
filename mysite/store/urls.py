from django.urls import path, include
from rest_framework import routers
from .views import *
from . import views

router = routers.DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cart-items')
router.register(r'order-items', OrderItemViewSet, basename='order-items')
router.register(r'addresses', AddressViewSet, basename='address')
router.register(r'payments', PaymentViewSet)
router.register(r'deliveries', DeliveryViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorites')
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'chat-messages', ChatMessageViewSet, basename='chat-messages')
router.register(r'articles', ArticleViewSet, basename='articles')

urlpatterns = [
    path('', include(router.urls)),
    path('users/search/', views.search_user, name='user_search'),

    # ✅ PRODUCTS
    path('products/', ProductListAPIView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),

    # ✅ CATEGORIES
    path('categories/', CategoryListAPIView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),

    # ✅ SUBCATEGORIES
    path('subcategories/', SubCategoryListAPIView.as_view(), name='subcategory_list'),
    path('subcategories/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='subcategory_detail'),

    # ✅ ORDERS
    path('orders/', OrderListAPIView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order_detail'),

    # ✅ RETURNS
    path('return-requests/', ReturnRequestListAPIView.as_view(), name='return_request_list'),
    path('return-requests/<int:pk>/', ReturnRequestDetailAPIView.as_view(), name='return_request_detail'),

    # ✅ PROMO
    path('promo-codes/', PromoCodeListAPIView.as_view(), name='promo_code_list'),
    path('promo-codes/<int:pk>/', PromoCodeDetailAPIView.as_view(), name='promo_code_detail'),

    # ✅ NOTIFICATIONS
    path('notifications/', NotificationListAPIView.as_view(), name='notification_list'),
    path('notifications/<int:pk>/', NotificationDetailAPIView.as_view(), name='notification_detail'),

    # ✅ PAYOUTS
    path('seller-payouts/', SellerPayoutListAPIView.as_view(), name='seller_payout_list'),
    path('seller-payouts/<int:pk>/', SellerPayoutDetailAPIView.as_view(), name='seller_payout_detail'),

    # ✅ AUTH
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    path('api/ext/activate/', ActivateStubView.as_view()),
]