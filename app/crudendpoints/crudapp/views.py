from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import request
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from .utils import get_from_db, save_models, upgrade_models, specify_errors
from .models import Customer, EmailPhone, Address
from .serializers import (
    CustomerSerializer,
    EmailPhoneSerializer,
    AddressSerializer,
    CombinedSerializer,
)


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def homepage(request) -> Response:
    """View represents GET endpoint"""
    return Response(template_name="homepage.html")


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def get_list(request: request) -> Response:
    """View represents GET endpoint"""
    customers = Customer.objects.all()
    return Response({"customers": customers}, template_name="listcustomers.html")


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def get_customer(request: request, customer_id: int) -> Response:
    """View represents GET endpoint"""
    customer = get_from_db(request, customer_id)
    contact = get_object_or_404(EmailPhone, person=customer).__dict__
    address = get_object_or_404(Address, person=customer).__dict__
    return Response(
        {"customer": customer, "contact": contact, "address": address},
        template_name="customerdetail.html",
    )


@api_view(["DELETE", "POST"])
@renderer_classes([TemplateHTMLRenderer])
def delete_customer(request: request, customer_id: int) -> Response:
    """View represents DELETE endpoint"""
    customer = get_from_db(request, customer_id)
    customer.delete()
    return Response(
        {"message": f"{customer} was successfully deleted!", "status": "success: 200"},
        status=200,
        template_name="message.html",
    )


class CreateCustomerView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "create.html"

    def get(self, request: request) -> Response:
        serializers = CombinedSerializer()
        return Response({"serializers": serializers})

    def post(self, request: request) -> Response:
        serializers = CombinedSerializer(data=request.data)
        if serializers.is_valid():
            save_models(serializers)
            return Response(
                {"message": "Customer was successfully created!", "status": "success"},
                status=200,
                template_name="message.html",
            )
        field_names = specify_errors(serializers)
        return Response(
            {
                "message": f"Customer was not created, input valid data! Invalid data in {field_names}",
                "status": "error: 400",
            },
            status=400,
            template_name="message.html",
        )


class UpdateCustomerView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "update.html"

    def get(self, request: request, customer_id: int) -> Response:
        customer = get_from_db(request, customer_id)
        contact = EmailPhone.objects.get(person=customer)
        address = Address.objects.get(person=customer)

        serializer = CombinedSerializer(
            {"customer": customer, "contact": contact, "address": address}
        )
        return Response({"customer": customer, "serializers": serializer})

    def post(self, request: request, customer_id: int) -> Response:
        serializer = CombinedSerializer(data=request.data)
        if serializer.is_valid():
            upgrade_models(serializer, customer_id)
            return Response(
                {
                    "message": "Customer details were successfully updated!",
                    "status": "success: 200",
                },
                status=200,
                template_name="message.html",
            )
        field_names = specify_errors(serializer)
        return Response(
            {
                "message": f"Customer details were not updated, input valid data in {field_names}!",
                "status": "error: 400",
            },
            status=400,
            template_name="message.html",
        )
