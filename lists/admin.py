from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "user",
        "count_rooms",
    )

    search_fields = ("name",)  # 검색 필드 추가

    filter_horizontal = ("rooms",)
