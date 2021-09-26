from math import ceil
from django.core import paginator  # 올림함수 import
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, Paginator
from django.views.generic import ListView
from django.urls import reverse
from . import models

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


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:  # 없는게 나오면 홈으로 돌려줌! 예외처리!
        return redirect(reverse("core:home"))
