from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db.models.fields import BLANK_CHOICE_DASH
from django.db.models.query_utils import check_rel_lookup_compatibility
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()

    pass


class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    inlines = (PhotoInline,)

    # fieldsets 이용하여 깔끔하게 정리

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "city", "country", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        (
            "More About the Space",
            {"fields": ("amenities", "facilities", "house_rules")},
        ),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        ("Last Details", {"fields": ("host",)}),
    )

    # list_display 속성을 사용하여 admin 페이지 꾸밈 (어떤 항목을 보여줄지)

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    # ordering = ("name", "price", "bedrooms")
    # ordering을 통해 정렬 우선 순위를 둘 수 있음

    list_filter = (
        "instant_book",
        "host__superhost",
        "host__gender",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    raw_id_fields = ("host",)

    search_fields = (
        "=city",
        "^host__username",  # host의 username에 접근
    )

    filter_horizontal = (  # ManyToManyField
        "amenities",
        "facilities",
        "house_rules",
    )

    def count_amenities(self, obj):
        print(obj.amenities.all())
        return "Potato"

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(
            f'<img width="50px" src="{obj.file.url}" />'
        )  # mark_safe import해서 html 그대로 사용하게 함

    get_thumbnail.short_description = "Thumbnail"
