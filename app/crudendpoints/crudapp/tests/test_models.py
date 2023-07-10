from django.test import TestCase
from ..models import Customer, EmailPhone, Address


class CustomerModelTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            firstname="John", lastname="Doe", birth="1991-01-01", sex="MALE"
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.firstname, "John")
        self.assertEqual(self.customer.lastname, "Doe")
        self.assertEqual(self.customer.birth, "1991-01-01")
        self.assertEqual(self.customer.sex, "MALE")
        self.assertEqual(str(self.customer), "John Doe customer has been created")

    def test_email_phone_creation(self):
        email_phone = EmailPhone.objects.create(
            person=self.customer, email="john.doe@example.com", phone="1234567890"
        )
        self.assertEqual(email_phone.person, self.customer)
        self.assertEqual(email_phone.email, "john.doe@example.com")
        self.assertEqual(email_phone.phone, "1234567890")
        self.assertEqual(
            str(email_phone),
            "John Doe customer has been created has added email john.doe@example.com and phone number 1234567890",
        )

    def test_address_creation(self):
        address = Address.objects.create(
            person=self.customer,
            country="USA",
            city="New York",
            province="NY",
            street="123 Main St",
            postcode="12345",
            house="1A",
            flat="4",
        )
        self.assertEqual(address.person, self.customer)
        self.assertEqual(address.country, "USA")
        self.assertEqual(address.city, "New York")
        self.assertEqual(address.province, "NY")
        self.assertEqual(address.street, "123 Main St")
        self.assertEqual(address.postcode, "12345")
        self.assertEqual(address.house, "1A")
        self.assertEqual(address.flat, "4")
        self.assertEqual(
            str(address),
            "John Doe customer has been created has address USA, 123 Main St, 1A",
        )
