# invoices/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Invoice, InvoiceDetail

class InvoiceAPITestCase(APITestCase):
    def setUp(self):
        self.invoice_data = {
            'date': '2024-01-13',
            'customer_name': 'Test Customer',
            'details': [
                {
                    'description': 'Product A',
                    'quantity': 2,
                    'unit_price': 10.0,
                    'price': 20.0
                },
                {
                    'description': 'Product B',
                    'quantity': 1,
                    'unit_price': 15.0,
                    'price': 15.0
                }
            ]
        }

        # Create the main invoice without details
        self.invoice = Invoice.objects.create(
            date=self.invoice_data['date'],
            customer_name=self.invoice_data['customer_name']
        )

    def test_create_invoice(self):
        url = reverse('invoice-list-create')

        # Set the invoice ID in the details data
        self.invoice_data['details'][0]['invoice'] = self.invoice.id
        self.invoice_data['details'][1]['invoice'] = self.invoice.id

        response = self.client.post(url, self.invoice_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)
        self.assertEqual(InvoiceDetail.objects.count(), 2)
