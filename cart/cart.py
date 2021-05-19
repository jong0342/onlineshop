from decimal import Decimal
from django.conf import settings
from shop.models import Product



class Cart(object):
    def __init__(self, request):  # 초기화 작업
        self.session = request.session
        cart = self.session.get(settings.CART_ID)
        if not cart:
            cart = self.session[settings.CART_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def __len__(self):          #
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):         # for문 사용시 요소 전달
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']

            yield item

    def add(self, product, quantity=1, is_update=False):  # is_update
        # session의 키값으로 호출하고 사용할 것이므로 string으로 변경시킴
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0, 'price': str(product.price)}

        if is_update:  # 제품 정보 수정할 경우
            self.cart[product_id]['quantity'] = quantity
        else:          # update가 아닌 경우에는 변경하게됨
            # else 부분은 상세 페이지에서 제품 수량을 증가 시키는 경우
            self.cart[product_id]['quantity'] += quantity

        self.save()  # 아래 save 메소드 호출

    def save(self):
        self.session[settings.CART_ID] = self.cart  # 정보 update
        self.session.modified = True                # 제품 변경 사항 있을시

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:              # 제품이 카트에 있는지 확인
            del(self.cart[product_id])          # 있는 경우 삭제함.
            self.save()                         # 삭제한 제품 사항을 db에 저장함

    def clear(self):                           # 장바구니를 싹 비움
        self.session[settings.CART_ID] = {}
        self.session['coupon_id'] = None
        self.session.modified = True

    # 장바구니에 들어있는 제품의 총합!
    def get_product_total(self):
        # Decimal()로 하지 않을 경우 unsupported error 발생
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())
