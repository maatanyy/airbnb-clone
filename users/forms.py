from django import forms


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)  #이렇게 하면 입력하면 점으로 나와서 보호됨
