from csv import DictReader
from io import TextIOWrapper

from shopapp.models import Product, Order


def save_csv_products(file, encoding):

    csv_file = TextIOWrapper(
        file,
        encoding,
    )

    reader = DictReader(csv_file)

    products = [
        Product(**row)
        for row in reader
    ]
    Product.objects.bulk_create(products)

    return products

def save_csv_orders(file, encoding):

    csv_file = TextIOWrapper(
        file,
        encoding,
    )

    reader = DictReader(csv_file, delimiter=',')

    for row in reader:
        orders = Order.objects.create(
            delivery_address=row["delivery_address"],
            promocode=row["promocode"],
            user_id=row["user_id"],
        )

        p = Product.objects.filter(id__in=list(map(int, row['products'].split())))

        orders.products.set(p)

        return orders
