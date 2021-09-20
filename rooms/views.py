from django.shortcuts import render
from . import models

# from datetime import datetime
# from django.http import HttpResponse

# Create your views here.


def all_rooms(request):
    # return HttpResponse(content=f"<h1>{now}</h1>")
    all_rooms = models.Room.objects.all()
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
        },
    )
