from tkinter.ttk import Widget
from django import forms
from . import models
from django.contrib.auth import password_validation

class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))  #이렇게 하면 입력하면 점으로 나와서 보호됨

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


class SignUpForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email",)

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': "First name"}),
            'last_name': forms.TextInput(attrs={'placeholder': "Last name"}),
            'email': forms.EmailInput(attrs={'placeholder': "Email"}),
        }

    #모델 폼 사용 전 사용하던 거임
    #first_name = forms.CharField(max_length=80)
    #last_name = forms.CharField(max_length=80)
    #email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Password"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Confirm Password"}))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                "That email is already taken", code="existing_user"
            )
        except models.User.DoesNotExist:
            return email
            
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    #장고 공식문서 modelform 참고 commit=False는 object는 생성하지만 database에 올리지 말라는 뜻
    #그냥 modelform 사용하고 admin으로 확인해보면 username 칸이 비어있음 그래서 save 함수를 
    # 조금 수정해서 username 이랑 password 구해주는 거임
    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()

#이 부분 빼야할수도
    def _post_clean(self):
        super()._post_clean()

        password = self.cleaned_data.get("password1")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error("password1", error) 
    
        

