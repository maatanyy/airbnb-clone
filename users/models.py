import email
import os
from random import choice
import uuid  #이메일에서 검증번호 보내기위해 추가
from django.conf import settings  #send_mail 함수 인자에서 사용하기위해 추가
from django.core.mail import send_mail
from django.utils.html import strip_tags
from statistics import mode
from django.template.loader import render_to_string   #template을 load해서 연결하는 역할
from django.contrib.auth.models import AbstractUser

# class User에서 model.model이 필요없고 다른걸 상속하기위해 이걸추가했다
from django.db import models
from django.forms import EmailInput

# Create your models here.


class User(AbstractUser):

    """Custom User Model"""  # 어떤 class인지 알려주기 위해 추가한거임

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "ko"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "English"), (LANGUAGE_KOREAN, "Korean"))

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = ((LOGIN_EMAIL, "Email"), (LOGIN_GITHUB, "Github"), (LOGIN_KAKAO, "Kakao"))

    avatar = models.ImageField(
        upload_to="avatars", blank=True
    )  # null은 database에서 blank는 form에서
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)

    bio = models.TextField(blank=True)  # default or null
    birthdate = models.DateField(blank=True, null=True)

    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN)

    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW)

    superhost = models.BooleanField(default=False)
    
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)

    login_method = models.CharField(max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)

    def verify_email(self):
        if self.email_verified is False:   #만약 이메일이 검증되었다면 아무것도 하지 않는다
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            ) #html_message로 메시지 묶고  
            #render_to_string을 사용해서 묶는 방법을 사용하면 css도 적용할수있고 좋다 해보니까 이거 개꿀인듯 
            send_mail(
                ("Verify Airbnb Account"),
                strip_tags(html_message),    #strip_tags이용해서 묶음
                settings.EMAIL_FROM, 
                [self.email], 
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return
    



