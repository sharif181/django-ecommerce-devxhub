# tests.py
from auth_app.models import Profile
from django.contrib.auth.models import User
from django.urls import reverse
from product_app.models import Product
from rest_framework import status
from rest_framework.test import APITestCase


class UserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.login_url = reverse('api-login')
        self.logout_url = reverse('api-logout')
        self.profile_url = reverse('api-profile')

    def test_login(self):
        response = self.client.post(self.login_url, {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'token')  # Adjust based on your response structure

    def test_logout(self):
        self.client.post(self.login_url, {'username': 'admin', 'password': 'admin'})
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_profile(self):
        self.client.post(self.login_url, {'username': 'admin', 'password': 'admin'})
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ProductTests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product', 
            description='test description',
            price=12.00, 
            stock=10
        )
        self.product_list_url = reverse('api-product_list')

    def test_product_list(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure the product is in the response

    def test_product_detail(self):
        response = self.client.get(reverse('api-product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

class OrderTests(APITestCase):
    def setUp(self):
        self.login_url = reverse('api-login')
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.post(self.login_url, {'username': 'admin', 'password': 'admin'})
        self.product = Product.objects.create(name='Test Product', description='test description', price=12.00, stock=True)
        self.order_url = reverse('api-order_list')

    def test_create_order(self):
        response = self.client.post(self.order_url, {
            'user': self.user.id,
            'first_name': 'first',
            'last_name': 'last',
            'email': 'test@gmail.com',
            'address': 'xyz',
            'postal_code': '4565',
            'city': 'dhaka',
            'paid': True,
            'order_status': 'Processing'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['city'], 'dhaka')

