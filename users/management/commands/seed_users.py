from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User

# We need to create custom commands because we want to automate putting data to our DB instead of manual clicking.


class Command(BaseCommand):

    help = "This command create many users"

    def add_arguments(self, parser):  # 장고 문서 참고
        parser.add_argument(
            "--number", default=1, type=int, help="How many users do you want create"
        )

    def handle(self, *args, **options):
        number = options.get("number", 2)
        seeder = Seed.seeder()
        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} users created!"))  # 확인문구
