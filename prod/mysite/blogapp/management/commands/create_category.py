from blogapp.models import Category
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Start create category")

        info = [
            (1, 'Action'),
            (2, 'Horror'),
            (3, 'Best action'),

        ]
        category = [
            Category(id=id, name=name) for id, name in info
        ]

        Category.objects.bulk_create(category)

        self.stdout.write("Done")