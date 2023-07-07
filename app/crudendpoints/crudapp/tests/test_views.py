from django.test import TestCase, RequestFactory, Client
from rest_framework.test import APITestCase
import json
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.test import APIRequestFactory
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from ..models import Customer
from ..views import homepage, CreateCustomerView, get_list

client = Client()


class HomepageViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_homepage_view(self):
        request = self.factory.get("/")
        response = homepage(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, "homepage.html")


class CreateCustomerViewTestCase(APITestCase):
    def test_create_customer(self):
        url = reverse("create_customer")
        data = {
            "firstname": "John",
            "lastname": "Doe",
            "birth": "1990-01-01",
            "sex": "MALE",
            "email": "john@example.com",
            "phone": "123456789",
            "country": "USA",
            "city": "New York",
            "province": "NY",
            "street": "123 Main St",
            "postcode": "10001",
            "house": "A",
            "flat": "1",
        }

        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Customer was successfully created!")

    def test_create_customer_invalid_data(self):
        url = reverse("create_customer")
        data = {
            "firstname": "John",
            "lastname": "Doe",
            "birth": "01-01-1991",
            "sex": "MALE",
            "email": "john@example.com",
            "phone": "123456789",
            "country": "USA",
            "city": "New York",
            "province": "NY",
            "street": "123 Main St",
            "postcode": "10001",
            "house": "A",
            "flat": "1",
        }

        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"],
            "Customer was not created, input valid data!",
        )



class GetListViewTestCase(APITestCase):
    def test_get_list(self):
        url = reverse('customers_list')
        
        Customer.objects.create(firstname='John', lastname='Doe', birth='1990-01-01', sex='MALE')
        Customer.objects.create(firstname='Jane', lastname='Smith', birth='1992-05-15', sex='FEMALE')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'listcustomers.html')
        self.assertEqual(len(response.data['customers']), 2)
