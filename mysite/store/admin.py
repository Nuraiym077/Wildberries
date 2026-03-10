from django.contrib import admin
from .models import *

class ArticleInline(admin.TabularInline):
    model = Article
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ReviewInline, ArticleInline]


class SubcategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubcategoryInline]

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 1


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    inlines = [ChatMessageInline]


admin.site.register(UserProfile)
admin.site.register(PromoCode)
admin.site.register(Payment)
admin.site.register(Delivery)
admin.site.register(ReturnRequest)
admin.site.register(SellerPayout)
admin.site.register(Favorite)
admin.site.register(Address)
admin.site.register(Notification)