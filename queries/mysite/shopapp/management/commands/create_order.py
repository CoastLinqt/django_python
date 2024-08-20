from django.core.management import BaseCommand
from shopapp.models import Order, Product
from django.contrib.auth.models import User
from typing import Sequence
from django.db import transaction


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Created order with products")
        user = User.objects.get(username="coastlineqt")
        products: Sequence[Product] = Product.objects.only("id").all()
        order, created = Order.objects.get_or_create(
            delivery_address="street Pushkin",
            promocode="promo8",
            user=user,
        )
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(f"Created order {order}")