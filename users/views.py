from dataclasses import field
import os
from re import L, template
from sre_constants import SUCCESS
import requests
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView #로그인 쉽게하는 방법 쓰기위해 FormView추가
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout  #추가
from . import forms, models, mixins
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
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


class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    #success_url = reverse_lazy("core:home")  # 이거때문에 reverse_lazy추가 ,form 가져올 때 url이 아직 불려지지 않아서 문제임
    
    # https://ccbv.co.uk/projects/Django/4.0/django.views.generic.edit/FormView/ 참고!!!!
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")

def log_out(request):
    messages.info(request,"See you later")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()  
        email = form.cleaned_data.get("email")   
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request,key): 
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""  #검증 후 secret은 지워줌
        user.save()
        #to do add success message
    except models.User.DoesNotExist:  #만약 이경우에는 email_secret이 key인 유저가 없다는 뜻!
        #to do add error message
        pass
    return redirect(reverse("core:home"))

def github_login(request):  #유저가 깃허브 로그인을 누르면 일어나는 일@@@@@@@
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user") 
    #redirect에서 요구하는 필수항목은 채워줘야한다. scope에 뭐가있나 더 찾아보자


class GithubException(Exception): #에러가 날경우 return redirect가 아닌 raise exception하고 error담당하게함 이게 더 코드가 깔끔하다
    pass


def github_callback(request):  #유저가 깃헙으로 이동한 싸이트에서 accept를 클릭할 경우@@@@@@ 
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(  #code를 가지고 token을 access하기위해서 또다른 requsest를 보냄@@@@@
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},  #그러면 이 줄에 의해서 우리에게 json을 준다@@@@@
            )
            token_json = token_request.json()   #json에 에러가 없나 확인하는과정@@@@@@@@
            error = token_json.get("error", None)
            if error is not None:         #에러가 있다면@@@@@@@@@
                raise GithubException("Can't get access token")
            else:       #만약 에러가없다면 그 json에서 token을 가져온다@@@@@@
                access_token = token_json.get("access_token")
                profile_request = api_request = requests.get( #이 토큰을 가지고 github api에 access한다@@@@@@
                    "https://api.github.com/user", 
                    headers={
                    "Authorization": f"token {access_token}",  #headers에서 token을 보내고@@@@
                    "Accept": "application/json",
                    },
                )
                profile_json = api_request.json()   #profile_json을 받는다@@@@
                username = profile_json.get('login', None)      #json안에 username이 있으면 문제없다는 뜻,,이걸 확인하는 과정
                if username is not None:
                    name = profile_json.get('name')
                    email = profile_json.get('email')
                    bio = profile_json.get('bio')
                    if name is None:
                        name = username
                    if email is None:
                        email = name
                    try:
                        user = models.User.objects.get(email=email)  
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(f"Please log in with: {user.login_method}")
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email, 
                            first_name=name, 
                            username=email, 
                            bio=bio, 
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your profile.")
        else:
            raise GithubException("Can't get code.")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("user:login"))



def kakao_login(request):
    REST_API_KEY = os.environ.get("KAKAO_ID")
    REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code"
    )


class KakaoException(Exception):
    pass

def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorzation code.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
        )

        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account["email"]  #카카오톡 로그인할려고 할 때 이메일 제공안하면 이 에러 발생
        if email is None:
            raise KakaoException("Please give an eamil.")
        profile = kakao_account["profile"]
        nickname = profile["nickname"]
        profile_image_url = profile['profile_image_url']
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"please log in with: {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image_url is not None:
                photo_request = requests.get(profile_image_url)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
            login(request, user)
            messages.success(request, f"Welcome back {user.first_name}")
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))

class UserProfileView(DetailView):
    
    model = models.User
    context_object_name = "user_obj"  #이걸 바꾼이유를 생각해보자 이걸 바꾸면 user_obj (상세페이지 주인의 정보얻음)


class UpdateProfileView(mixins.LoggedInOnlyView ,SuccessMessageMixin, UpdateView):

    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )
    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate"}
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        form.fields["gender"].widget.attrs = {"placeholder": "Gender"}
        form.fields["bio"].widget.attrs = {"placeholder": "Bio"}
        form.fields["language"].widget.attrs = {"placeholder": "Language"}
        form.fields["currency"].widget.attrs = {"placeholder": "Currency"}
        return form

class UpdatePasswordView(mixins.EmailLoginOnlyView, mixins.LoggedInOnlyView, SuccessMessageMixin, PasswordChangeView):

    template_name = "users/update-password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {"placeholder": "Confirm new password"}
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


#Django 공식문서 session 검색 참고!!!
@login_required   #delete가 된다면 host였다는 거고 아니면 이제 host가 되고 싶다는 뜻
def switch_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))






