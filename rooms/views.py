from math import ceil
from django.core import paginator  # 올림함수 import
from django.core.paginator import EmptyPage, Paginator
from django.views.generic import ListView, DetailView  # ListView 사용하기 위해 추가
from . import models
from django.shortcuts import render
from django_countries import countries

# from django.http import Http404
# from django.shortcuts import render

# from datetime import datetime
# from django.http import HttpResponse

# Create your views here.


class HomeView(ListView):
    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
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


def search(request):
    city = request.GET.get("city", "Anywhere")  # ,뒤에는 default
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    room_types = models.RoomType.objects.all()
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    s_amenities = request.GET.getlist("amenities")   #하나를 가져오고 싶은게 아니니까 getlist를 쓴다!!
    s_facilities = request.GET.getlist("facilities")  #하나를 가져오고 싶은게 아니니까 getlist를 쓴다!!
    instant = bool(request.GET.get("instant", False))   #필터에서 true false로 체크하니까 bool해줬음
    superhost = bool(request.GET.get("superhost", False))

    form = {"city": city, 
            "s_country": country, 
            "s_room_type": room_type, 
            "price": price, 
            "guests": guests, 
            "bedrooms": bedrooms, 
            "beds": beds, 
            "baths": baths,
            "s_amenities" : s_amenities,
            "s_facilities" : s_facilities,
            "instant" : instant,
            "superhost" :superhost,
            }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {"countries": countries, "room_types": room_types, "amenities": amenities, "facilities":facilities}

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type   #room_type 은 foreignkey이다

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms
    
    if beds != 0:
        filter_args["bedrooms__gte"] = beds
    
    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if superhost is True:
        filter_args["host__superhost"] = True   

    #if len(s_amenities) > 0:
     #   for s_amenity in s_amenities:
        #    filter_args["amenities__pk"] = int(s_amenity)
    #if len(s_facilities) > 0:
        #for s_facility in s_facilities:
            #filter_args["facilities__pk"] = int(s_facility)


    rooms = models.Room.objects.filter(**filter_args)

    if len(s_amenities) > 0:
        for s_amenity in s_amenities: 
            rooms = rooms.filter(amenities__pk=int(s_amenity))   #이부분 위 주석처리한 것과 잘 비교하자 이렇게하면 예를들어 amenity 2개 고르면
            # 하나만 해당되느 것도 나왔는데 이렇게 하면 둘다 해당되는 것만 나오게 된다. filter.filter 요런느낌!!

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            rooms = rooms.filter(facilities__pk=int(s_facility))

    return render(
        request,
        "rooms/search.html",
        {**form, **choices, "rooms": rooms}  # 여기서 form+chocies로 하면 안됨 **이용해서 한다
    )
