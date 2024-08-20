from blogapp.models import Article, Tag
from django.core.management import BaseCommand
from typing import Sequence


class Command(BaseCommand):

    def handle(self, *args, **options):

        self.stdout.write("Start crate article")

        tags: Sequence[Tag] = Tag.objects.only("id").all()
        article, created = Article.objects.get_or_create(
            title="Hello2!",
            content="man!",
            author_id=1,
            category_id=3,
        )
        for tag in tags:
            article.tags.add(tag)
        article.save()

        self.stdout.write("Done")