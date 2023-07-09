from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from .models import Customer, EmailPhone, Address
from .serializers import CustomerSerializer, EmailPhoneSerializer, AddressSerializer


# Create your views here.
@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def homepage(request) -> Response:
    """View represents GET endpoint"""
    return Response(template_name="homepage.html")


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def get_list(request) -> Response:
    """View represents GET endpoint"""
    customers = Customer.objects.all()
    return Response({"customers": customers}, template_name="listcustomers.html")


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def get_customer(request, customer_id) -> Response:
    """View represents GET endpoint"""
    customer = Customer.objects.get(id=customer_id)
    contact = EmailPhone(person=customer)
    address = Address(person=customer)
    return Response(
        {"customer": customer, "contact": contact, "address": address},
        template_name="customerdetail.html",
    )


class CreateCustomerView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "create.html"

    def get(self, request):
        form1 = CustomerSerializer()
        form2 = EmailPhoneSerializer()
        form3 = AddressSerializer()
        return Response({"form1": form1, "form2": form2, "form3": form3})

    def post(self, request):
        form1 = CustomerSerializer(data=request.data)
        form2 = EmailPhoneSerializer(data=request.data)
        form3 = AddressSerializer(data=request.data)
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            form1.save()
            form2.save()
            form3.save()
            return Response(
                {"message": "Customer was successfully created!", "status": "success"},
                status=200,
                template_name="message.html",
            )

        return Response(
            {
                "message": "Customer was not created, input valid data!",
                "status": "error",
            },
            status=400,
            template_name="message.html",
        )
