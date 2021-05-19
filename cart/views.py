from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST  # post로만 처리가 가능한 녀석

from shop.models import Product
from .forms import AddProductForm
from .cart import Cart


@require_POST  # 함수형 뷰를 실행하기전 실행되는 놈인데요.
def add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # 클라이언트 -> 서버로 데이터를 전달
    # 유효성 검사, injection 전처리
    # 노출하는 폼과 유효성 검사를 할때 사용함 즉, 사용자로부터 뭔가를 입력받아 처리하는건 form으로 처리함
    form = AddProductForm(request.POST)
    if form.is_valid():                 # 유효성 검사 진행함.
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'], is_update=cd['is_update'])

    return redirect('cart:detail')


def remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')


def detail(request):
    cart = Cart(request)
    for product in cart:
        product['quantity_form'] = AddProductForm(
            initial={'quantity': product['quantity'], 'is_update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
