# customers/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from customers.models import Customer
from rest_framework_simplejwt.tokens import RefreshToken


class CustomerTests(APITestCase):

    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass123')

        self.token = self.get_jwt_token()

        # Set the authentication header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def get_jwt_token(self):
        refresh = RefreshToken.for_user(self.user)

        return str(refresh.access_token)

    def test_create_customer(self):
        url = reverse('customer-list')
        data = {
            'user': self.user.id,
            'name': 'John Doe',
            'code': 'CUST123',
            'phone_number': '1234567890'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_customers(self):
        Customer.objects.create(user=self.user, name='John Doe', code='CUST123', phone_number='1234567890')
        url = reverse('customer-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_customer(self):
        customer = Customer.objects.create(user=self.user, name='John Doe', code='CUST123', phone_number='1234567890')
        url = reverse('customer-detail', kwargs={'pk': customer.id})
        data = {
            "user": customer.id,
            'name': 'Jane Doe',
            'code': 'CUST456',
            'phone_number': '0987654321'
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Jane Doe')

    def test_delete_customer(self):
        customer = Customer.objects.create(user=self.user, name='John Doe', code='CUST123', phone_number='1234567890')
        url = reverse('customer-detail', kwargs={'pk': customer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
