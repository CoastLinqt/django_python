from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from timeit import default_timer
from django.contrib.auth.models import Group
from .models import Product, Order
from django.views.generic import (ListView,
                                  DetailView,
                                  DeleteView,
                                  CreateView,
                                  UpdateView)
from django.views import View
from .forms import GroupForm
from django.urls import reverse_lazy


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

        }
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm,
            "groups": Group.objects.prefetch_related('permissions').all(),

        }
        return render(request=request, template_name='shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetails(DetailView):
    template_name = "shopapp/product-details.html"
    model = Product
    context_object_name = "product"


class ProductsList(ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = "products"

    queryset = Product.objects.filter(archived=False)


class ProductCreateView(CreateView):
    model = Product
    fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:products_list")


class ProductUpdateView(UpdateView):
    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:products_details",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

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


class OrderListView(ListView):
    queryset = Order.objects.select_related('user').prefetch_related('products')


class OrderDetailView(DetailView):
    queryset = Order.objects.select_related('user').prefetch_related('products')






