from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Debt, Client, Consumer, CollectionAgency

class DebtListViewTests(APITestCase):
    def setUp(self):
        """Set up test data before each test."""
        # Create a client and consumer for debt relationships
        self.agency = CollectionAgency.objects.create(name="AKTOS_TEST")
        self.client1 = Client.objects.create(reference="CLIENT1", collection_agency=self.agency)
        self.consumer1 = Consumer.objects.create(name="John Doe", address="123 Main St", ssn="123-45-6789")
        self.consumer2 = Consumer.objects.create(name="John Cena", address="432 Main St", ssn="987-45-6789")
        self.consumer3 = Consumer.objects.create(name="Michael Scofield", address="English, Fitz or Percy ", ssn="320-00-99")

        # Create debts with different balances
        self.debt1 = Debt.objects.create(client=self.client1, consumer=self.consumer1, balance=100, status="ACTIVE")
        self.debt2 = Debt.objects.create(client=self.client1, consumer=self.consumer2, balance=500, status="INACTIVE")
        self.debt3 = Debt.objects.create(client=self.client1, consumer=self.consumer3, balance=1000, status="PAID_IN_FULL")

        # Define the endpoint URL
        self.url = reverse("collection_agency:debt-list")

    def test_filter_by_min_balance(self):
        """Should return debts with balance >= min_balance."""
        response = self.client.get(self.url, {'min_balance': 500})

        # Validate response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse JSON response
        data = response.json()

        # Expect only debts with balance >= 500 (debt2 and debt3)
        self.assertTrue(all(float(item["balance"]) >= 500 for item in data))
        self.assertEqual(len(data), 2)  # Expecting debt2 (500) and debt3 (1000)

