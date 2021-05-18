from decimal import Decimal
from django.conf import settings

from shop.models import Product

class Cart(object):
    def __init__(self, requsest):
        self.session = requsest.session
        cart = self.session.get(settings.CART_ID)
        if not cart:
            cart = self.sesstion[settings.CART_ID] = {}
        self.cart = cart

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)