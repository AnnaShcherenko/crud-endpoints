from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path(
        "create_customer/", views.CreateCustomerView.as_view(), name="create_customer"
    ),
    path("customers_list/", views.get_list, name="customers_list"),
    path("customer/<int:customer_id>/", views.get_customer, name="customer_details"),
    path(
        "customer/delete/<int:customer_id>/",
        views.delete_customer,
        name="delete_customer",
    ),
    path(
        "customer/<int:customer_id>/update",
        views.UpdateCustomerView.as_view(),
        name="update_customer",
    ),
]
