from blogapp.models import Author
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Start create author")

        info = [
            (1, 'Viktor', 'Hello'),
            (2, 'Stepan', 'Hello'),
            (3, 'Misha', 'Hello'),

        ]
        authors = [
            Author(id=id, name=name, bio=bio) for id, name, bio in info
        ]

        Author.objects.bulk_create(authors)

        self.stdout.write("Done")