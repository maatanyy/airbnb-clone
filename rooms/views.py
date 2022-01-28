from math import ceil
from django.core import paginator  # 올림함수 import
from django.core.paginator import EmptyPage, Paginator
from django.views.generic import ListView, DetailView  # ListView 사용하기 위해 추가
from . import models, forms
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
    
    form = forms.SearchForm()

    return render(request,"rooms/search.html", {"form" : form})
