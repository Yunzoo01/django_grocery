from django.contrib import admin
from .models import User, Product, Basket

# 사용자 모델 등록
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_customer', 'is_staff', 'email')
    list_filter = ('is_customer', 'is_staff')
    search_fields = ('username', 'email')

# 제품 모델 등록
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

# 장바구니 모델 등록
@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'status')
    list_filter = ('status',)
    search_fields = ('customer__username', 'product__name')