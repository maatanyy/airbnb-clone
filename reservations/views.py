from ast import Try
import datetime
from re import M
from django.shortcuts import render
from django.views.generic import View
from rooms import models as room_models
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from . import models
import reservations


class CreateError(Exception):
    pass

# Create your views here.
def create(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year, month, day)
        room = room_models.Room.objects.get(pk=room)
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "Can't Reserve That Room")
        return redirect(reverse("core:home"))
    except models.BookedDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(View):  #그냥 view를 상속한 이유, get_method를 컨트롤 하고 싶어서
    def get(self, pk):
        try:
            reservation = models.Reservation.objects.get(pk=pk)
        except: