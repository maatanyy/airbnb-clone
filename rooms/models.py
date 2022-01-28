from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField

# django_countires의 CountryField를 사용하기 위해
from core import models as core_models
from users import models as user_models

# host 에서 Foreignkey를 통해 user model과 연결시키기 위해
# Create your models here.


class AbstractItem(core_models.TimeStampedModel):
    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    class Meta:
        verbose_name = "Room Type"

    # ordering = ["name"]     ordering을 통해 보이는 순서 변경 가능


class Amenity(AbstractItem):

    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """Faclity Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_ph")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField(help_text="How many people will be staying?")  #help_text붙이면 더 자세히 알기 좋음
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(  # host는 user의 연장이니까 Foreignkey를 이용해서 만듬 물론 이걸 위해서 위에 import했음
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # self.city = str.capitalize(self.city)  도시 이름의 앞글자를 대문자로
        self.city = (
            self.city.title()
        )  # 도시 이름이 두 단어 이상인 경우도 있기 때문에 이걸 쓰면 됨, upper는 모든 단어가 대문자로 됨
        super().save(*args, **kwargs)

    def get_absolute_url(
        self,
    ):  # 어떤 url을 갖고있던 지정하는곳으로 이동 (어드민페이지에서!), 오버로드임, 즉 어드민 페이지에서만 변화보임
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()  # 모든 room이 가지는 review를 얻음
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews))
        return 0
