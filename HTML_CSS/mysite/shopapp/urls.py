from django.urls import path

from .views import shop_index, groups_list, products_list, order_list, create_product, create_order

app_name = "shopapp"

urlpatterns = [
    path("", shop_index, name="index"),
    path("groups/", groups_list, name="groups_list"),
    path("products/", products_list, name="products_list"),
    path("products/create", create_product, name="create_product"),
    path("orders/", order_list, name="order_list"),
    path("orders/create", create_order, name="create_order")


]