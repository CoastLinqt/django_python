from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (ShopIndexView,
                    # GroupListView,
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
                    ProductsDataExportView,
                    OrdersDataExportView,
                    ProductViewSet,
                    OrderViewSet,
                    LatestProductsFeed,
                    UserOrdersListView,
                    )

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    # path("groups/", GroupListView.as_view(), name="groups_list"),
    path("products/", ProductsList.as_view(), name="products_list"),
    path("products/export/", ProductsDataExportView.as_view(), name="products-export"),
    path("products/create/", ProductCreateView.as_view(), name="create_product"),
    path("products/<int:pk>/", ProductDetails.as_view(), name="products_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="products_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="products_delete"),
    path("products/latest/feed", LatestProductsFeed(), name="products-feed"),
    path("users/<int:pk>/orders/", UserOrdersListView.as_view(), name="user_order"),
    path("users/<int:pk>/orders/export", OrdersDataExportView.as_view(), name="user_order_export"),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="order_detail"),
    path("orders/<int:pk>/update", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete", OrderDeleteView.as_view(), name="order_delete"),
    # path("orders/export/", OrdersDataExportView.as_view(), name="orders-export"),
    path("orders/create/", OrderCreateView.as_view(), name="create_order"),
    path("api/", include(routers.urls)),


]