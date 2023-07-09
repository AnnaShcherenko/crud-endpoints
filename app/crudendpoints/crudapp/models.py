from django.db import models

SEX = (("FEMALE", "F"), ("MALE", "M"))


class Customer(models.Model):
    firstname = models.CharField(max_length=100, null=False, blank=False)
    lastname = models.CharField(max_length=100, null=False, blank=False)
    birth = models.DateField(max_length=10, null=False, blank=False)
    sex = models.CharField(choices=SEX, max_length=6)

    def __str__(self) -> str:
        return f"{self.firstname} {self.lastname} customer has been created"


class EmailPhone(models.Model):
    person = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)

    def __str__(self) -> str:
        return (
            f"{self.person} has added email {self.email} and phone number {self.phone}"
        )


class Address(models.Model):
    person = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True)
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    province = models.CharField(max_length=30, null=True, blank=True)
    street = models.CharField(max_length=30)
    postcode = models.CharField(max_length=10)
    house = models.CharField(max_length=6, null=True, blank=True)
    flat = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.person} has address {self.country}, {self.street}, {self.house}"
