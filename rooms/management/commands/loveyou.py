from django.core.management.base import BaseCommand

# We need to create custom commands because we want to automate putting data to our DB instead of manual clicking.


class Command(BaseCommand):

    help = "This command tells me that he loves me"

    def add_arguments(self, parser):
        parser.add_argument(
            "--times", help="How many times do you want me to tell you that I love you?"
        )

    def handle(self, *args, **options):
        times = options.get("times")
        for t in range(0, int(times)):
            self.stdout.write(self.style.SUCCESS("I love you"))
