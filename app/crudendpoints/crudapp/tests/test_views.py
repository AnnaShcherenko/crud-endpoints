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

    def test_get_customer(self):
        url = reverse("customer_details", args=[self.customer.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "customerdetail.html")

    def test_get_nonexistent_customer(self):
        url = reverse("customer_details", args=[3])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTemplateUsed(response, "message.html")
        self.assertEqual(response.data["message"], "Customer doesn't exist!")
        self.assertEqual(response.data["status"], "error")


class DeleteCustomerViewTestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            firstname="John", lastname="Doe", birth="1990-01-01", sex="MALE"
        )

    def test_delete_customer(self):
        url = reverse("delete_customer", args=[self.customer.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "message.html")
        self.assertEqual(
            response.data["message"], f"{self.customer} was successfully deleted!"
        )
        self.assertEqual(response.data["status"], "success")
        self.assertFalse(Customer.objects.filter(id=self.customer.id).exists())

    def test_delete_nonexistent_customer(self):
        url = reverse("delete_customer", args=[3])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTemplateUsed(response, "message.html")
        self.assertEqual(response.data["message"], "Customer doesn't exist!")
        self.assertEqual(response.data["status"], "error")


class UpdateCustomerViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
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
        request = self.factory.get(self.url)
        view = UpdateCustomerView.as_view()
        response = view(request, customer_id=self.customer.id)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update.html")
        self.assertIsInstance(response.data["serializer"], CombinedSerializer)

    def test_post_valid_data(self):
        updated_customer_data = {
            "firstname": "Jane",
            "lastname": "Smith",
            "birth": "1995-02-15",
            "sex": "FEMALE",
        }
        updated_contact_data = {
            "email": "jane.smith@example.com",
            "phone": "9876543210",
        }
        updated_address_data = {
            "country": "Canada",
            "city": "Toronto",
            "street": "456 Maple Ave",
            "postcode": "M1N 2P3",
        }

        request = self.factory.post(
            self.url,
            data={
                "customer": updated_customer_data,
                "contact": updated_contact_data,
                "address": updated_address_data,
            },
        )
        view = UpdateCustomerView.as_view()
        response = view(request, customer_id=self.customer.id)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "message.html")
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(EmailPhone.objects.count(), 1)
        self.assertEqual(Address.objects.count(), 1)
        updated_customer = Customer.objects.get(id=self.customer.id)
        updated_contact = EmailPhone.objects.get(person=updated_customer)
        updated_address = Address.objects.get(person=updated_customer)
        self.assertEqual(updated_customer.firstname, updated_customer_data["firstname"])
        self.assertEqual(updated_customer.lastname, updated_customer_data["lastname"])
        self.assertEqual(
            updated_customer.birth.strftime("%Y-%m-%d"), updated_customer_data["birth"]
        )
        self.assertEqual(updated_customer.sex, updated_customer_data["sex"])
        self.assertEqual(updated_contact.email, updated_contact_data["email"])
        self.assertEqual(updated_contact.phone, updated_contact_data["phone"])
        self.assertEqual(updated_address.country, updated_address_data["country"])
        self.assertEqual(updated_address.city, updated_address_data["city"])
        self.assertEqual(updated_address.street, updated_address_data["street"])
        self.assertEqual(updated_address.postcode, updated_address_data["postcode"])

    def test_post_invalid_data(self):
        invalid_customer_data = {
            "firstname": "Jane",
            "lastname": "",  # Invalid, empty value
            "birth": "1995-02-15",
            "sex": "FEMALE",
        }
        invalid_contact_data = {
            "email": "jane.smith@example.com",
            "phone": "",  # Invalid, empty value
        }
        invalid_address_data = {
            "country": "",
            "city": "Toronto",
            "street": "456 Maple Ave",
            "postcode": "M1N 2P3",
        }

        request = self.factory.post(
            self.url,
            data={
                "customer": invalid_customer_data,
                "contact": invalid_contact_data,
                "address": invalid_address_data,
            },
        )
        view = UpdateCustomerView.as_view()
        response = view(request, customer_id=self.customer.id)
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "message.html")
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(EmailPhone.objects.count(), 1)
        self.assertEqual(Address.objects.count(), 1)
        self.assertFormError(
            response, "serializer", "customer.lastname", "This field is required."
        )
        self.assertFormError(
            response, "serializer", "contact.phone", "This field is required."
        )
        self.assertFormError(
            response, "serializer", "address.country", "This field is required."
        )
