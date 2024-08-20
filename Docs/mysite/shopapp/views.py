"""
В этом модуле лежат различные наборы представлений.

Разные view интернет магазина: по товарам, заказам итд

"""

from django.shortcuts import render, reverse
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseRedirect,
    JsonResponse)
from timeit import default_timer
from django.contrib.auth.models import Group
from .models import Product, Order, ProductImage
from django.views.generic import (ListView,
                                  DetailView,
                                  DeleteView,
                                  CreateView,
                                  UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views import View
# from .forms import GroupForm
from .forms import ProductForm
from django.urls import reverse_lazy
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse


@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений дял действий над Product
    Полный CRUD для сущностей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]

    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "id",
        "name",
        "price",
        "discount",
    ]

    @extend_schema(

        summary='Get one product by ID',
        description='Retrieves **product** returns 404 if not found',
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description='Empty response product by id not found'),

        },
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


@extend_schema(description="Order views CRUD")
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = [
        "delivery_address",
        "promocode",
        "user",
        "products",

    ]

    ordering_fields = [
        "id",
        "delivery_address",
        "user",
        "products",

    ]


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer,
            "products": products,
            "items": 5,

        }
        return render(request, 'shopapp/shop-index.html', context=context)


# class GroupListView(View):
#     def get(self, request: HttpRequest) -> HttpResponse:
#         context = {
#             "form": GroupForm,
#             "groups": Group.objects.prefetch_related('permissions').all(),
#
#         }
#         return render(request=request, template_name='shopapp/groups-list.html', context=context)
#
#     def post(self, request: HttpRequest):
#         form = GroupForm(request.POST)
#         if form.is_valid():
#             form.save()
#
#         return redirect(request.path)


class ProductDetails(PermissionRequiredMixin, DetailView):
    permission_required = ["shopapp.view_product"]
    template_name = "shopapp/product-details.html"
    # model = Product
    queryset = Product.objects.prefetch_related('images')
    context_object_name = "product"


class ProductsList(PermissionRequiredMixin, ListView):
    permission_required = ["shopapp.view_product"]
    template_name = 'shopapp/products-list.html'
    model = Product
    context_object_name = "products"

    queryset = Product.objects.filter(archived=False)


class ProductCreateView(PermissionRequiredMixin, CreateView):

    permission_required = ["shopapp.add_product"]

    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form=form)


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ["shopapp.change_product"]
    login_url = 'shopapp/products-list.html'

    model = Product
    # fields = "name", "price", "description", "discount", "preview"
    template_name_suffix = "_update_form"
    form_class = ProductForm

    def form_valid(self, form):
        response = super().form_valid(form=form)
        if form.instance.created_by == self.request.user:
            for image in form.files.getlist('images'):
                ProductImage.objects.create(
                    product=self.object,
                    image=image
                )

            return response
        else:

            return render(request=self.request, template_name="shopapp/update_user_haven't_product.html")

    def get_success_url(self):
        return reverse(
            "shopapp:products_details",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    @extend_schema(
        summary='Create order',
        description='**order** create')
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)



class OrderCreateView(CreateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    success_url = reverse_lazy("shopapp:order_list")




class OrderUpdateView(UpdateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    template_name = "shopapp/order_update_form.html"

    def get_success_url(self, **kwargs):
        return reverse(
            "shopapp:order_detail",
            kwargs={"pk": self.object.pk}
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:order_list")


class OrderListView(LoginRequiredMixin, ListView):
    queryset = Order.objects.select_related('user').prefetch_related('products')


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ["shopapp.view_order"]
    queryset = Order.objects.select_related('user').prefetch_related('products')


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by("pk").all()

        products_data = [{
            "pk": product.pk,
            "name": product.name,
            "price": product.price,
            "archived": product.archived,
            "created_by": product.created_by.id
        }
            for product in products
        ]

        return JsonResponse({"products": products_data})


class OrdersDataExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by('pk').all()

        orders_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,

                "user": order.user.pk,
                "products": [p.pk for p in order.products.all()],
            }
            for order in orders
        ]

        return JsonResponse({"orders": orders_data})



