from blogapp.models import Tag
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Start create tag")

        info = [
            (1, 'Action 1'),
            (2, 'Horror 1'),
            (3, 'Best action 1'),

        ]
        tags = [
            Tag(id=id, name=name) for id, name in info
        ]

        Tag.objects.bulk_create(tags)

        self.stdout.write("Done")