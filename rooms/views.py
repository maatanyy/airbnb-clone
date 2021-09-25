from math import ceil
from django.core import paginator  # 올림함수 import
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, Paginator
from django.views.generic import ListView
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
