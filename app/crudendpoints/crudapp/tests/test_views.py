from django.test import TestCase, RequestFactory, Client
from rest_framework.test import APITestCase
import json
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.test import APIRequestFactory
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from ..models import Customer, EmailPhone, Address
from ..utils import get_from_db
from ..views import homepage, CreateCustomerView, get_list, UpdateCustomerView

client = Client()


class HomepageViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_homepage_view(self):
        request = self.factory.get("/")
        response = homepage(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, "homepage.html")


from django.urls import reverse
from rest_framework.test import APITestCase


class CreateCustomerViewTest(APITestCase):
    def test_create_customer_valid_data(self):
        url = reverse("create_customer")
        data = {
            "customer": {
                "firstname": "John",
                "lastname": "Doe",
                "birth": "1990-01-01",
                "sex": "MALE",
            },
            "contact": {
                "email": "john@example.com",
                "phone": "1234567890",
            },
            "address": {
                "country": "USA",
                "city": "New York",
                "street": "123 Main St",
                "postcode": "12345",
            },
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Customer was successfully created!")

    def test_create_customer_invalid_data(self):
        url = reverse("create_customer")
        data = {}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["status"], "error: 400")
        self.assertIn("message", response.data)


class GetListViewTestCase(APITestCase):
    def test_get_list(self):
        url = reverse("customers_list")
        Customer.objects.create(
            firstname="John", lastname="Doe", birth="1990-01-01", sex="MALE"
        )
        Customer.objects.create(
            firstname="Jane", lastname="Smith", birth="1992-05-15", sex="FEMALE"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "listcustomers.html")
        self.assertEqual(len(response.data["customers"]), 2)


class GetCustomerViewTestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            firstname="John", lastname="Doe", birth="1990-01-01", sex="MALE"
        )
        self.contact = EmailPhone.objects.create(
            person=self.customer, email="john.doe@example.com", phone="1234567890"
        )
        self.address = Address.objects.create(
            person=self.customer,
            country="USA",
            city="New York",
            street="123 Main St",
            postcode="10001",
        )
        self.url = reverse("customer_details", args=[self.customer.id])

    def test_get_customer(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customerdetail.html")


class DeleteCustomerViewTestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            firstname="John", lastname="Doe", birth="1990-01-01", sex="MALE"
        )

    def test_delete_customer(self):
        url = reverse("delete_customer", args=[self.customer.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "message.html")
        self.assertEqual(
            response.data["message"], f"{self.customer} was successfully deleted!"
        )
        self.assertEqual(response.data["status"], "success: 200")
        self.assertFalse(Customer.objects.filter(id=self.customer.id).exists())


class UpdateCustomerViewTest(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            firstname="John", lastname="Doe", birth="1990-01-01", sex="MALE"
        )
        self.contact = EmailPhone.objects.create(
            person=self.customer, email="john.doe@example.com", phone="1234567890"
        )
        self.address = Address.objects.create(
            person=self.customer,
            country="USA",
            city="New York",
            street="123 Main St",
            postcode="10001",
        )
        self.url = reverse("update_customer", args=[self.customer.id])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update.html")

    def test_post_valid_data(self):
        data = {
            "customer": {
                "firstname": "John",
                "lastname": "Doe",
                "birth": "1990-01-01",
                "sex": "MALE",
            },
            "contact": {
                "email": "john@example.com",
                "phone": "1234567890",
            },
            "address": {
                "country": "USA",
                "city": "New York",
                "street": "123 Main St",
                "postcode": "12345",
            },
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "message.html")
        self.assertEqual(response.context["status"], "success: 200")

    def test_post_invalid_data(self):
        data = {
            "customer": {
                "firstname": "John",
                "lastname": "",
                "birth": "01-01-1991",
                "sex": "MALE",
            },
            "contact": {
                "email": "john@example.com",
                "phone": "1234567890",
            },
            "address": {
                "country": "USA",
                "city": "New York",
                "street": "123 Main St",
                "postcode": "12345",
            },
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "message.html")
        self.assertEqual(response.context["status"], "error: 400")
