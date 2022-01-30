from statistics import mode
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

    avatar = models.ImageField(
        upload_to="avatars", blank=True
    )  # null은 database에서 blank는 form에서
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)

    bio = models.TextField(blank=True)  # default or null
    birthdate = models.DateField(blank=True, null=True)

    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, blank=True , default=LANGUAGE_KOREAN)

    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, blank=True , default=CURRENCY_KRW)

    superhost = models.BooleanField(default=False)
    
    email_confirmed = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="", blank=True)

    def verify_email(self):
        pass
