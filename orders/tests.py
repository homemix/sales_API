# orders/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from customers.models import Customer
from django.contrib.auth.models import User
from orders.models import Order
from rest_framework_simplejwt.tokens import RefreshToken


class OrderTests(APITestCase):

    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass123')
        self.customer = Customer.objects.create(user=self.user, name='John Doe', code='CUST123',
                                                phone_number='1234567890')
        self.token = self.get_jwt_token()

        # Set the authentication header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def get_jwt_token(self):
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_create_order(self):
        url = reverse('order-list')
        data = {
            'item': 'Laptop',
            'amount': 1200.00,
            'customer': self.customer.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
