from django.views import View
from django.views.generic import FormView  #로그인 쉽게하는 방법 쓰기위해 FormView추가
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout  #추가
from . import forms, models
import os
import requests
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

    def form_valid(self, form):
        form.save()   
        email = form.cleaned_data.get("email")   #저장후 자동 로그인 
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
                raise GithubException()
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
                            raise GithubException()
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
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        #send error message
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
            raise KakaoException()
        access_token = token_json.get("access_token")
        profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
        )

        profile_json = profile_request.json()
        gender = profile_json.get("gender")
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account["email"]
        if email is None:
            raise KakaoException()
        profile = kakao_account["profile"]
        nickname = profile["nickname"]
        profile_image_url = profile['profile_image_url']
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException()
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
            login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException:
        return redirect(reverse("users:login"))


