from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'review', ReviewViewSet)
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cart-items')
router.register(r'order-items', OrderItemViewSet, basename='order-items')
router.register(r'address', AddressViewSet, basename='address')
router.register(r'payment', PaymentViewSet)
router.register(r'delivery', DeliveryViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorites')
router.register(r'chat', ChatViewSet, basename='chat')
router.register(r'chat-messages', ChatMessageViewSet, basename='chat-messages')
router.register(r'product-images', ProductImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('product/', ProductListAPIView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('subcategory/', SubCategoryListAPIView.as_view(), name='subcategory_list'),
    path('subcategory/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='subcategory_detail'),
    path('orders/', OrderListAPIView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order_detail'),
    path('return-requests/', ReturnRequestListAPIView.as_view(), name='return_request_list'),
    path('return-requests/<int:pk>/', ReturnRequestDetailAPIView.as_view(), name='return_request_detail'),
    path('promo-codes/', PromoCodeListAPIView.as_view(), name='promo_code_list'),
    path('promo-codes/<int:pk>/', PromoCodeDetailAPIView.as_view(), name='promo_code_detail'),
    path('notifications/', NotificationListAPIView.as_view(), name='notification_list'),
    path('notifications/<int:pk>/', NotificationDetailAPIView.as_view(), name='notification_detail'),
    path('seller-payouts/', SellerPayoutListAPIView.as_view(), name='seller_payout_list'),
    path('seller-payouts/<int:pk>/', SellerPayoutDetailAPIView.as_view(), name='seller_payout_detail'),
]