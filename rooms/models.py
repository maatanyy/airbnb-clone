from django.db import models
from django_countries.fields import CountryField

# django_countires의 CountryField를 사용하기 위해
from core import models as core_models
from users import models as user_models

# host 에서 Foreignkey를 통해 user model과 연결시키기 위해
# Create your models here.


class AbstractItem(core_models.TimeStampedModel):
    """Abstract Item"""

    class Meta:
        abstract = True


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
