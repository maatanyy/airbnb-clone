from django import forms
from django_countries.fields import CountryField  #이름 그대로,, 쓰기위해 추가
from . import models

class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")  #widget 사용해서 form모양 바꿀수 있음, ex)widget=forms.Textarea
    country = CountryField(default="KR").formfield()
    price = forms.IntegerField(required=False)
    room_type = forms.ModelChoiceField(required=False, empty_label="Any Kind", queryset=models.RoomType.objects.all())
    price = forms.IntegerField(required=False)
    guest = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(required=False, queryset=models.Amenity.objects.all(), widget=forms.CheckboxSelectMultiple) #여러개 고를 수 있어야해서 ModelMultipleChoiceField사용
    facilities = forms.ModelMultipleChoiceField(required=False, queryset=models.Facility.objects.all(), widget=forms.CheckboxSelectMultiple)