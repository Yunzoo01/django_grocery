from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Basket
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# 홈 페이지
def home(request):
    return render(request, 'store/home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print(f"DEBUG: username={username}, password={password}")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print(f"DEBUG: Authenticated user - {user.username}, is_customer={user.is_customer}, is_staff={user.is_staff}")
            login(request, user)
            if user.is_staff:
                return redirect('manage_baskets')  # 직원 페이지
            elif user.is_customer:
                return redirect('product_list')  # 고객 페이지
        else:
            print("DEBUG: Authentication failed for username={username}")
            return render(request, 'store/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'store/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import user_passes_test

@login_required
@user_passes_test(lambda u: u.is_customer)
def customer_page(request):
    return render(request, 'store/customer_page.html')

@login_required
@user_passes_test(lambda u: u.is_staff)
def staff_page(request):
    return render(request, 'store/staff_page.html')

# 제품 목록 페이지
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# 장바구니에 제품 추가 (고객 전용)
@login_required
@user_passes_test(lambda u: u.is_customer)
def add_to_basket(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        Basket.objects.create(customer=request.user, product=product, quantity=quantity)
        return redirect('basket')
    return render(request, 'store/add_to_basket.html', {'product': product})

# 장바구니 관리 (직원 전용)
@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_baskets(request):
    baskets = Basket.objects.filter(status='pending')
    return render(request, 'store/manage_baskets.html', {'baskets': baskets})

# 고객의 장바구니 보기
@login_required
@user_passes_test(lambda u: u.is_customer)
def view_basket(request):
    baskets = Basket.objects.filter(customer=request.user)  # 로그인한 고객의 장바구니만 가져오기
    return render(request, 'store/view_basket.html', {'baskets': baskets})

# 장바구니 승인/거절 (직원 전용)
@login_required
@user_passes_test(lambda u: u.is_staff)
def approve_basket(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id)
    if request.method == 'POST':
        action = request.POST.get('action')  # 'approve' 또는 'deny' 값
        if action == 'approve':
            basket.status = 'approved'
        elif action == 'deny':
            basket.status = 'denied'
        basket.save()
        return redirect('manage_baskets')
    return render(request, 'store/manage_baskets.html')


# 고객의 구매 내역 보기
@login_required
@user_passes_test(lambda u: u.is_customer)
def purchase_history(request):
    purchases = Basket.objects.filter(customer=request.user, status='approved')  # 승인된 항목만 가져오기
    return render(request, 'store/purchase_history.html', {'purchases': purchases})