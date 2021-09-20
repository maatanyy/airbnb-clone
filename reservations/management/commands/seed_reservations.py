import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations import models as reservation_models
from users import models as user_models
from rooms import models as room_models

# 체크인 날짜는 지금, 체크 아웃은 랜덤으로 며칠 뒤로 설정하는데 이걸 하기 위해서 datetime, tiemdelta를 import 함
NAME = "reservations"


class Command(BaseCommand):

    help = "This command create many {NAME}"

    def add_arguments(self, parser):  # 장고 문서 참고
        parser.add_argument(
            "--number", default=2, type=int, help="How many {NAME} do you want create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            reservation_models.Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 25)),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))  # 확인문구
