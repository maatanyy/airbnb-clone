from math import ceil
from django.core import paginator  # 올림함수 import
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models

# from datetime import datetime
# from django.http import HttpResponse

# Create your views here.


def all_rooms(request):
    # return HttpResponse(content=f"<h1>{now}</h1>")
    page = request.GET.get("page")
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)
    rooms = paginator.get_page(page)
    return render(request, "rooms/home.html", {"page": rooms})
