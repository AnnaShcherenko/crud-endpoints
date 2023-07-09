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
                "status": "error",
            },
            status=400,
            template_name="message.html",
        )


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


def upgrade_models(serializer):
    validated_data = serializer.validated_data
    customer_data = validated_data["customer"]
    contact_data = validated_data["contact"]
    address_data = validated_data["address"]

    customer.firstname = customer_data.get("firstname", customer.firstname)
    customer.lastname = customer_data.get("lastname", customer.lastname)
    customer.birth = customer_data.get("birth", customer.birth)
    customer.sex = customer_data.get("sex", customer.sex)
    customer.save()

    contact.email = contact_data.get("email", contact.email)
    contact.phone = contact_data.get("phone", contact.phone)
    contact.save()

    address.country = address_data.get("country", address.country)
    address.city = address_data.get("city", address.city)
    address.province = address_data.get("province", address.province)
    address.street = address_data.get("street", address.street)
    address.postcode = address_data.get("postcode", address.postcode)
    address.house = address_data.get("house", address.house)
    address.flat = address_data.get("flat", address.flat)
    address.save()
