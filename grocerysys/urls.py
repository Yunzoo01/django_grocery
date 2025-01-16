"""
URL configuration for grocerysys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views  # store 앱의 뷰 가져오기

urlpatterns = [
    path('admin/', admin.site.urls),  # 관리자 페이지
    path('', views.home, name='home'),  # 홈 페이지
    path('products/', views.product_list, name='product_list'),  # 제품 목록
    path('basket/add/<int:product_id>/', views.add_to_basket, name='add_to_basket'),  # 장바구니 추가
    path('baskets/manage/', views.manage_baskets, name='manage_baskets'),  # 장바구니 관리
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('customer/', views.customer_page, name='customer_page'),
    path('staff/', views.staff_page, name='staff_page'),
    path('basket/', views.view_basket, name='basket'),
    path('basket/approve/<int:basket_id>/', views.approve_basket, name='approve_basket'),
    path('purchase-history/', views.purchase_history, name='purchase_history'),
]