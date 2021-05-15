from django.shortcuts import render, get_object_or_404, redirect, redirect, reverse
from django.contrib import messages
import urllib, os
# Create your views here.
from .models import *

def product_in_category(request, category_slug=None):
    current_category= None
    categories = Category.objects.all()
    products = Product.objects.filter(available_display=True)
    if category_slug:
        current_category = get_object_or_404(Category,slug=category_slug)
        products = products.filter(category=current_category)
    return render(request, 
                    'shop/list.html',
                    {
                        'current_category':current_category,
                        'categories':categories,
                        'products':products
                    })

def product_detail(request, id, product_slug=None):
    product = get_object_or_404(Product, id=id, slug=product_slug)
    return render(request, 'shop/detail.html', {'product':product})


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={REDIRECT_URI}&response_type=code"
    )


def kakao_login(request):
    try:
        if request.user.is_authenticated:
            raise SocialLoginException("User already logged in")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"

        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        )
    except KakaoException as error:
        messages.error(request, error)
        return redirect("core:home")
    except SocialLoginException as error:
        messages.error(request, error)
        return redirect("core:home")
