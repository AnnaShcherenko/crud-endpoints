from django.db.models import fields
from rest_framework import serializers
from .models import Customer, EmailPhone, Address

SEX = (("FEMALE", "F"), ("MALE", "M"))


class CustomerSerializer(serializers.ModelSerializer):
    birth = serializers.DateField(input_formats=["%Y-%m-%d"])
    sex = serializers.ChoiceField(choices=SEX)

    class Meta:
        model = Customer
        fields = ("firstname", "lastname", "birth", "sex")
        extra_kwargs = {
            "firstname": {"required": True},
            "lastname": {"required": True},
            "birth": {"required": True},
        }


class EmailPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailPhone
        fields = ("email", "phone")


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("country", "city", "province", "street", "postcode", "house", "flat")


class CombinedSerializer(serializers.Serializer):
    customer = CustomerSerializer()
    contact = EmailPhoneSerializer()
    address = AddressSerializer()
