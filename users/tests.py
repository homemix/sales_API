# users/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # Create a user to authenticate against
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # URL for user registration
        # self.registration_url = reverse('dj-rest-auth-registration')
        self.registration_url = reverse('rest_register')
        # URL for login and obtaining a JWT token
        self.token_url = reverse('token_obtain_pair')

    def test_register_user(self):
        """Test that a user can register successfully"""
        registration_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        response = self.client.post(self.registration_url, registration_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_login_and_get_jwt_token(self):
        """Test that a user can log in and receive a JWT token"""
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpassword'
        }, format='json')
        print(response)

        # Check for a successful response and that it returns tokens
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Store the access token for authenticated requests
        self.access_token = response.data['access']


    def test_fail_login_with_wrong_credentials(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'wronguser',
            'password': 'wrongpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
