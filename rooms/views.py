from math import ceil
from django.core import paginator  # 올림함수 import
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, Paginator
from . import models

# from datetime import datetime
# from django.http import HttpResponse

# Create your views here.


def all_rooms(request):
    # return HttpResponse(content=f"<h1>{now}</h1>")
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)
    try:
        rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", {"page": rooms})
    except EmptyPage:
        return redirect(
            "/"
        )  # 예외의 경우 home으로 돌려보내줌 ,, except Exception 으로 해도되나 어떤 에러를 어케 처리할지 다룰줄 아는게 중요

    return render(request, "rooms/home.html", {"page": rooms})
