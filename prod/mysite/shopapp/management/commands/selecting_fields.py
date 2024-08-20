from django.core.management import BaseCommand
from shopapp.models import Product
from django.contrib.auth.models import User
from typing import Sequence


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Created order with products")
        user_info = User.objects.values_list("username", flat=True)
        print(list(user_info))
        for user in user_info:
            print(user)

        # product_values = Product.objects.values("pk", "name")
        # for p_values in product_values:
        #     print(p_values)

        self.stdout.write("Done")