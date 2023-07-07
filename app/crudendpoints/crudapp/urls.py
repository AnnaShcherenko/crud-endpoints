from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path(
        "create_customer/", views.CreateCustomerView.as_view(), name="create_customer"
    ),
    path("customers_list", views.get_list, name="customers_list"),
    # path("customerdetail/<int:customer_id>", views.get_customer, name="customer_detail")
]
