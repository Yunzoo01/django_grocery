from django.contrib.auth.models import AbstractUser
from django.db import models

# 사용자 모델
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)  # 고객 여부
    is_staff = models.BooleanField(default=False)  # 직원 여부

    def __str__(self):
        return self.username

# 제품 모델
class Product(models.Model):
    name = models.CharField(max_length=255)  # 제품 이름
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 제품 가격

    def __str__(self):
        return self.name

# 장바구니 모델
class Basket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),  # 대기 중
        ('approved', 'Approved'),  # 승인됨
        ('denied', 'Denied'),  # 거절됨
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_customer': True})  # 고객 연결
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # 제품 연결
    quantity = models.PositiveIntegerField()  # 제품 수량
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # 상태

    def __str__(self):
        return f'{self.customer.username} - {self.product.name} - {self.status}'