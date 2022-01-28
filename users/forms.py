from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)  #이렇게 하면 입력하면 점으로 나와서 보호됨

    #def clean_email(self):  #이름 임의로 지은거 아님 clean이 있어야함 검사할 때 
    #    email = self.cleaned_data.get("email")
    #    try:
    #       models.User.objects.get(username=email)
    #        return email
    #    except models.User.DoesNotExist:
    #        raise forms.ValidationError("User does not exist")  #raise 에러 한곳에서 에러가 뜬다!!
    
    def clean(self):   #이름 임의로 지은거 아님 clean이 있어야함 검사할 때 
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data  #여기가 중요 cleaned_data를 return 해야한다 clean을 썻을경우
            else:
                self.add_error("password", forms.ValidationError("Password is wrong")) 
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist")) 


#만약 clean_email ,clean_password따로 만드는 방식쓰면 error를 raise써서 하지만 이렇게 clean으로 할경우에는 에러를 따로만들어준다


class SignUpForm(forms.Form):

    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput)


