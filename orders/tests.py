# orders/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from customers.models import Customer
from django.contrib.auth.models import User
from orders.models import Order
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch


class OrderTests(APITestCase):

    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass123')
        self.customer = Customer.objects.create(user=self.user, name='John Doe', code='CUST123',
                                                phone_number='+254234567890')
        self.token = self.get_jwt_token()

        # Set the authentication header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def get_jwt_token(self):
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    @patch('services.sending_sms.SendSMS')
    def test_create_order(self, MockSendSMS):
        mock_sms_service = MockSendSMS.return_value
        mock_sms_service.success = False
        url = reverse('order-list')
        data = {
            'item': 'Laptop',
            'amount': 1200.00,
            'customer': self.customer.id
        }
        response = self.client.post(url, data, format='json')
        if mock_sms_service.success is not False:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # Fetch the order instance from the database
            order = Order.objects.get(id=response.data['id'])

            # Test the __str__ method of the Order model
            self.assertEqual(str(order), f"Order {order.id} for Laptop by {order.customer}")

        else:
            # Check that the response status is HTTP 503 Service Unavailable due to SMS failure
            self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    def test_get_orders(self):
        Order.objects.create(item='Laptop', amount=1200.00, customer=self.customer)
        url = reverse('order-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_order(self):
        order = Order.objects.create(item='Laptop', amount=1200.00, customer=self.customer)
        url = reverse('order-detail', kwargs={'pk': order.id})
        data = {
            'item': 'Smartphone',
            'amount': 800.00,
            'customer': self.customer.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['item'], 'Smartphone')

    def test_delete_order(self):
        order = Order.objects.create(item='Laptop', amount=1200.00, customer=self.customer)
        url = reverse('order-detail', kwargs={'pk': order.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
