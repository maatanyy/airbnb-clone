from django.views import View
from django.views.generic import FormView  #로그인 쉽게하는 방법 쓰기위해 FormView추가
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout  #추가
from . import forms

# Create your views here.

# 로그인 어려운 방법
# class LoginView(View):

#     def get(self, request):
#         form = forms.LoginForm(initial={"email": "min@naver.com"})
#         return render(request, "users/login.html", {"form": form})

#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(request, "users/login.html", {"form": form})


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")  # 이거때문에 reverse_lazy추가 ,form 가져올 때 url이 아직 불려지지 않아서 문제임
    
    # https://ccbv.co.uk/projects/Django/4.0/django.views.generic.edit/FormView/ 참고!!!!
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    
def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        'first_name': "Min Sung",
        'last_name': "Noh",
        'email': "min@naver.com",
    }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User already exists with that email")
        except models.User.DoesNotExist:
            return email
    
    def clean_password1(self):
        password = self.clean_data.get("password")
        password1 = self.clean_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password