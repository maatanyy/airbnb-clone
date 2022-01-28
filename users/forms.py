from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)  #이렇게 하면 입력하면 점으로 나와서 보호됨

    def clean_email(self):  #이름 임의로 지은거 아님 clean이 있어야함 검사할 때 
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")
    
    def clean_password(self):   #이름 임의로 지은거 아님 clean이 있어야함 검사할 때 
        print("clean password")




