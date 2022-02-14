from ast import Expression, Try
from dataclasses import field
from math import ceil
from msilib.schema import File
from click import confirmation_option
from django.core import paginator  # 올림함수 import
from django.core.paginator import EmptyPage, Paginator
from django.views.generic import ListView, DetailView, View, UpdateView, CreateView, FormView # ListView 사용하기 위해 추가
from . import models, forms
from django.shortcuts import redirect, render, reverse
from django_countries import countries
from django.core.paginator import Paginator
from users import mixins as user_mixins
from django.http import Http404
from django.contrib.auth.decorators import login_required  #deletephoto에서 데코레이터 추가하기 위해 추가
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# from django.http import Http404
# from django.shortcuts import render

# from datetime import datetime
# from django.http import HttpResponse

# Create your views here.


class HomeView(ListView):
    """HomeView Definition"""

    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


# def room_detail(request, pk):
#   try:
#        room = models.Room.objects.get(pk=pk)
#        return render(request, "rooms/detail.html", {"room": room})
#    except models.Room.DoesNotExist:  # 없는게 나오면 홈으로 돌려줌! 예외처리!
#        raise Http404()  # return 이 아니라 raise해줘야한다


class RoomDetail(DetailView):

    """RoomDetail Definition"""

    model = models.Room

class SearchView(View):

    def get(self, request):
        country = request.GET.get("country")
    
        if country:

            form = forms.SearchForm(request.GET)  #무슨데이터인지는 모르지만 어떤 데이터를 가지고 있다, #form = forms.SearchForm 에 request.GET만 추가하면 form이 기억한다!!

            if form.is_valid():  #만약 에러가 없다면
                city = form.cleaned_data.get("city")  
                country = form.cleaned_data.get("country")
                price = form.cleaned_data.get("price")
                room_type = form.cleaned_data.get("room_type")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type   #room_type 은 foreignkey이다

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms
        
                if beds is not None:
                    filter_args["bedrooms__gte"] = beds
        
                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True
                
                rooms = models.Room.objects.filter(**filter_args)
                for amenity in amenities:
                    rooms = rooms.filter(amenities=amenity)
                for facility in facilities:
                    rooms = rooms.filter(facilities=facility)

                qs = models.Room.objects.filter(**filter_args).order_by("created")  #paginator를 쓰기위해서 시작 끝을 알아야하니까 이렇게 알려줌

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(request,"rooms/search.html", {"form": form, "rooms": rooms})

        else:  #종종 빈 데이터 폼을 보여줘야 할 때 즉 첫 form을 가져와야 할 때
            form = forms.SearchForm()

        
        return render(request,"rooms/search.html", {"form": form })

class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset = None):
        room = super().get_object(queryset = queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()  #내방 아닌거 수정할라고 url로 들가면 못하게 막는 보안과정
        return room  

class RoomPhotosView(user_mixins.LoggedInOnlyView, RoomDetail):  #Room의 DetailView라고 생각

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset = None):
        room = super().get_object(queryset = queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()  #내방 아닌거 수정할라고 url로 들가면 못하게 막는 보안과정
        return room  


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            #photo =models.Photo   #1번방법
            #photo.delete()        #이렇게 해도됨
            models.Photo.objects.filter(pk=photo_pk).delete() #필터써서 쿼리셋에서 pk=photo_pk해서 하나만 해당되게 함
            messages.success(request,"Photo Deleted")
        return redirect(reverse("rooms:photos", kwargs={'pk': room_pk})) 
    except models.Room.DoesNotExist:  #방이 존재하지 않는다면 홈으로 redirect하면 됨
        return redirect(reverse("core:home"))

class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"  #문서에 pk_url_kwarg가 있음 pk가 아닌 photo_pk를 찾게함
    success_message = "Photo Updated"
    fields = ("caption",) #fields는 tupple이 되게 string이믄 안댐

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView): #우리가 Form을 새로 만들어줬기 때문에 CreateView가 아닌 FormView사용

    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("rooms:photos", kwargs={'pk': pk}))

class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        form.save_m2m()
        messages.success(self.request, "Room Uploaded")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))



