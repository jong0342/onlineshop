from django import forms

# 1. 클라이언트 화면에 입력 폼을 만들어주기 위해서
# 2. 클라이언트가 입력한 데이터에 대한 전처리


class AddProductForm(forms.Form):
    quantity = forms.IntegerField()
    # BooleanField의 경우  필수로 required 파라미터를 False로 지정함.
    is_update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    # widget 파라미터는 고객이 보고 판단하는 것이 아닌 백단에서 판단하기에 HiddenInput값으로 지정함
