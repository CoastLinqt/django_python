"""
В этом модуле лежат различные наборы представлений.

Разные view интернет магазина: по товарам, заказам итд

"""
import logging
from django.shortcuts import render, reverse
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseRedirect,
    JsonResponse)
from timeit import default_timer
from csv import DictWriter
from django.contrib.auth.models import Group, User
from .models import Product, Order, ProductImage
from django.views.generic import (ListView,
                                  DetailView,
                                  DeleteView,
                                  CreateView,
                                  UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views import View
from myauth.models import Profile
# from .forms import GroupForm
from .forms import ProductForm
from django.urls import reverse_lazy
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.parsers import MultiPartParser
from .common import save_csv_products
from django.contrib.syndication.views import Feed
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.shortcuts import get_object_or_404

log = logging.getLogger(__name__)


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

    @action(methods=['get'], detail=False)
    def download_csv(self,request: Request):

        response = HttpResponse(content_type="text/csv")
        filename = "products-export.csv"
        response["Content-Disposition"] = f"attachment; filename={filename}-export.csv"

        queryset = self.filter_queryset(self.get_queryset())

        fields = [
            "name",
            "description",
            "price",
            "discount",
        ]

        queryset = queryset.only(*fields)

        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow(
                {
                    field: getattr(product, field) for field in fields
                }
            )

        return response

    @action(detail=False,
            methods=['post'],
            parser_classes=[MultiPartParser],)
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES["file"].file,
            encoding=request.encoding
        )

        serializer = self.get_serializer(products, many=True)

        return Response(serializer.data)

    @method_decorator(cache_page(60 * 2))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)


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
    # @method_decorator(cache_page(60 * 2))
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
        log.debug("Products for shop index: %s", products)
        log.info("Rendering shop index")

        print("")

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


class LatestProductsFeed(Feed):
    title = "Product"
    description = "Updates on changes and addition product"
    link = reverse_lazy("blogapp:products_list")

    def items(self):
        return (Product.objects.filter(archived=False).order_by("-created_at")
                )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]

    def item_link(self, item: Product):
        return reverse("blogapp:products_details", kwargs={"pk": item.pk})


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


class UserOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "shopapp/order_list_user.html"

    def get_queryset(self):
        self.owner = get_object_or_404(Profile.objects.select_related('user'), id=self.kwargs["pk"])

        self.queryset = Order.objects.select_related('user').filter(user_id=self.owner.user_id)

        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)
        for user in self.queryset:
            data["owner"] = user.user
            return data


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


class OrderDetailView(DetailView):

    queryset = Order.objects.select_related('user').prefetch_related('products')


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by("pk").all()

            products_data = [{
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,

            }
                for product in products
            ]
            cache.set(cache_key, products_data, 300)
        return JsonResponse({"products": products_data})


class OrdersDataExportView(View):

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        cache_key = "orders_data_export"
        orders_data = cache.get(cache_key)

        self.owner = get_object_or_404(Profile.objects.select_related('user'), id=self.kwargs["pk"])

        queryset = Order.objects.order_by('-pk').select_related('user').filter(user_id=self.owner.user_id)
        if orders_data is None:

            orders_data = [
                {
                    "pk": order.id,
                    "delivery_address": order.delivery_address,
                    "promocode": order.promocode,

                    "user": order.user.pk,
                    "products": [p.pk for p in order.products.all()],
                }
                for order in queryset
            ]
            cache.set(cache_key, orders_data, 100)

        return JsonResponse({"orders": orders_data})



