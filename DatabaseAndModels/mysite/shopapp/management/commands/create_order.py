from django.core.management import BaseCommand
from shopapp.models import Order
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Created order")
        user = User.objects.get(username="admin")
        order = Order.objects.get_or_create(
            delivery_address="street Pushkin",
            promocode="SALE",
            user=user,
        )
        self.stdout.write(f"Created order {order}")