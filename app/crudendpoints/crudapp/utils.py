from rest_framework.decorators import renderer_classes
from rest_framework.response import Response
from rest_framework import request
from rest_framework.renderers import TemplateHTMLRenderer
from .models import Customer, EmailPhone, Address
from .serializers import (
    CustomerSerializer,
    EmailPhoneSerializer,
    AddressSerializer,
    CombinedSerializer,
)


@renderer_classes([TemplateHTMLRenderer])
def get_from_db(request: request, customer_id: int) -> Customer:
    try:
        return Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response(
            {
                "message": "Customer doesn't exist!",
                "status": "error: 404",
            },
            status=404,
            template_name="message.html",
        )


def specify_errors(serializer):
    default_errors = serializer.errors
    field_names = []
    for subfield in default_errors.items():
        if isinstance(subfield[1], dict):
            for field_name, field_errors in subfield[1].items():
                field_names.append(field_name)

        elif isinstance(subfield[1], list):
            field_names.extend(subfield[1])
    return field_names


def save_models(serializer):
    validated_data = serializer.validated_data
    customer_data = validated_data["customer"]
    contact_data = validated_data["contact"]
    address_data = validated_data["address"]
    customer_model = Customer(**customer_data)
    customer_model.save()

    contact_data["person"] = customer_model
    contact_model = EmailPhone(**contact_data)
    contact_model.save()

    address_data["person"] = customer_model
    address_model = Address(**address_data)
    address_model.save()


def upgrade_models(serializer, customer_id):
    validated_data = serializer.validated_data
    customer_data = validated_data.get("customer", {})
    contact_data = validated_data.get("contact", {})
    address_data = validated_data.get("address", {})

    customer = get_from_db(request, customer_id)
    contact = EmailPhone.objects.get(person=customer)
    address = Address.objects.get(person=customer)

    for key, value in customer_data.items():
        setattr(customer, key, value)
    customer.save()
    for key, value in contact_data.items():
        setattr(contact, key, value)
    contact.save()
    for key, value in address_data.items():
        setattr(address, key, value)
    address.save()
