from dataclasses import field
from math import ceil
from django.core import paginator  # 올림함수 import
from django.core.paginator import EmptyPage, Paginator
from django.views.generic import ListView, DetailView, View, UpdateView  # ListView 사용하기 위해 추가
from . import models, forms
from django.shortcuts import render
from django_countries import countries
from django.core.paginator import Paginator

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

class EditRoomView(UpdateView):

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



