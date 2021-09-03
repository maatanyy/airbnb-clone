from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


# Register your models here.
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    fieldsets = UserAdmin.fieldsets + (  # admin 페이지에 fieldsets 추가!
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )

    # list_display = (
    #     "username",
    #     "gender",
    #     "language",
    #     "currency",
    #     "superhost",
    # )  # list_display 기억하자 이걸로 adminpage에서 보이는거 설정

    # list_filter = (
    #     "language",
    #     "currency",
    #     "superhost",
    # )  # list_filter 이걸로 admin 페이지 옆에 관리하기 쉽게 필터 생김
