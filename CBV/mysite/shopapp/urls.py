from django.urls import path

from .views import (ShopIndexView,
                    GroupListView,
                    ProductDetails,
                    ProductsList,
                    OrderCreateView,
                    OrderListView,
                    OrderDetailView,
                    OrderUpdateView,
                    OrderDeleteView,
                    ProductCreateView,
                    ProductUpdateView,
                    ProductDeleteView,
                    )

app_name = "shopapp"

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupListView.as_view(), name="groups_list"),
    path("products/", ProductsList.as_view(), name="products_list"),
    path("products/create", ProductCreateView.as_view(), name="create_product"),
    path("products/<int:pk>/", ProductDetails.as_view(), name="products_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="products_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="products_delete"),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="order_detail"),
    path("orders/<int:pk>/update", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete", OrderDeleteView.as_view(), name="order_delete"),
    path("orders/create", OrderCreateView.as_view(), name="create_order")


]