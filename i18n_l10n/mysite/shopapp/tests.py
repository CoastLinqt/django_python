import json
import random
from django.test import TestCase
from .utils import add_two_numbers
from django.urls import reverse
from string import ascii_letters
from random import choices
from .models import Product, User, Order
from django.conf import settings
from django.contrib.auth.models import Permission, Group


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 4)
        self.assertEqual(result, 6)


class ProductCreateViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.product_name = "".join(choices(ascii_letters, k=10))

        cls.user = User.objects.create_superuser(username="Vlad", password="1234567")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        Product.objects.filter(name=cls.product_name).delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_product_create(self):
        response = self.client.post(
            reverse("shopapp:create_product"),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "goof table",
                "discount": "10",
            },
        )

        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_superuser(username="Vlad", password="1234567")
        cls.product = Product.objects.create(name="Best Product")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.product.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:products_details", kwargs={"pk": self.product.pk})
        )


        self.assertEqual(response.status_code, 200)

    def test_check_contain(self):
        response = self.client.get(
            reverse("shopapp:products_details", kwargs={"pk": self.product.pk})
        )

        self.assertContains(response, self.product.discount)


class ProductsListViewTestVase(TestCase):
    fixture = [
        "shopapp_products.json",
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_superuser(username="Vlad", password="1234567")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"))
        expected_products = list(Product.objects.filter(archived=False).all())
        actual_products = list(response.context["products"])
        self.assertSequenceEqual(
            [p.pk for p in expected_products],
            [p.pk for p in actual_products]
        )
        self.assertTemplateUsed(response, "shopapp/products-list.html")


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_superuser(username="Vlad", password="1234567")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_order_view(self):

        response = self.client.get(reverse("shopapp:order_list"))

        self.assertContains(response, "Orders")

    def test_orders_view_bot_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:order_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'shopapp_user.json',
        "shopapp_products.json",

    ]

    def test_get_products_view(self):
        response = self.client.get(reverse("shopapp:products-export"))

        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()

        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
                "created_by": product.created_by.id

            }
            for product in products
        ]

        products_data = response.json()
        self.assertEqual(products_data["products"], expected_data)


class OrderDetailView(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="georgeboewn", password="1234567")
        permission_logentry = Permission.objects.get(
            codename="view_order",
        )

        cls.user.user_permissions.add(permission_logentry)


    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.order = Order.objects.create(delivery_address='Hello', promocode='200Hi', user=self.user)

    def tearDown(self):
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(reverse("shopapp:order_detail", kwargs={"pk": self.order.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)

        received_data = response.context['object'].pk

        expected_data = self.order.pk

        self.assertEqual(received_data, expected_data)


class OrdersExportViewTestCase(TestCase):
    fixtures = [
        'shopapp_user.json',
        'shopapp_products.json',
        'shopapp_orders.json',

    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="Myname", password="1234567", is_staff=True)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_get_orders_view(self):
        response = self.client.get(reverse("shopapp:orders-export"))

        self.assertEqual(response.status_code, 200)

        orders = Order.objects.order_by("pk").all()

        expected_data = [
        {
            "pk": order.pk,
            "delivery_address": order.delivery_address,
            "promocode": order.promocode,
            "user_id": order.user.pk,
            "products": [p.pk for p in order.products.all()],
        }
            for order in orders
        ]
        orders_data = response.json()

        self.assertEqual(orders_data["orders"], expected_data)



