from django.core.management.base import BaseCommand
from library.seed import create_initial_data

class Command(BaseCommand):

    def handle(self, *args, **options):
        create_initial_data()
        self.stdout.write(
            self.style.SUCCESS("Database created.")
        )