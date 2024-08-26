from django.test import TestCase, Client
from django.urls import reverse
from user.models import User, ConfirmCode
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import json
from utils import hashcode

class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.user_confirm_url = reverse('user_confirm')

    def test_register_success(self):
        data = {
            'username': 'testuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'email': 'testuser@example.com'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status_code'], 1)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        user = User.objects.get(username='testuser')
        self.assertTrue(check_password('strongpassword123', user.password))

    def test_register_username_exists(self):
        User.objects.create(username='testuser', password='password', email='testuser@example.com')
        data = {
            'username': 'testuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'email': 'newuser@example.com'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status_code'], 2)

    def test_register_email_exists(self):
        User.objects.create(username='anotheruser', password='password', email='testuser@example.com')
        data = {
            'username': 'testuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'email': 'testuser@example.com'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status_code'], 3)

    def test_register_password_mismatch(self):
        data = {
            'username': 'testuser',
            'password1': 'strongpassword123',
            'password2': 'differentpassword',
            'email': 'testuser@example.com'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status_code'], 4)

    def test_user_confirm_success(self):
        user = User.objects.create(username='testuser', password='password', email='testuser@example.com', user_confirm=False)
        code = ConfirmCode.objects.create(user=user, code='testcode')
        response = self.client.get(f'{self.user_confirm_url}?code=testcode')
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.user_confirm)
        self.assertFalse(ConfirmCode.objects.filter(code='testcode').exists())

    def test_user_confirm_invalid_code(self):
        response = self.client.get(f'{self.user_confirm_url}?code=invalidcode')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incorrect.html')

class UserAuthTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            password=make_password('testpassword'),
            email='testuser@example.com',
            user_confirm=True
        )
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.get_user_info_url = reverse('get_user_info')


    def test_login_success(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status_code'], 1)
        self.assertTrue(self.client.session['is_login'])

    def test_login_wrong_password(self):
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status_code'], 5)

    def test_login_unverified_account(self):
        self.user.user_confirm = False
        self.user.save()
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status_code'], 4)

    def test_get_user_info_not_logged_in(self):
        response = self.client.post(self.get_user_info_url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status_code'], 2)

class PasswordResetTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            password=make_password('testpassword'),
            email='testuser@example.com',
            user_confirm=True
        )
        self.reset_password_url = reverse('reset_password')
        self.reset_password_confirm_url = reverse('reset_password_confirm', args=['testcode'])
        self.confirm_code = ConfirmCode.objects.create(user=self.user, code='testcode')

    # def test_reset_password_success(self):
    #     response = self.client.post(self.reset_password_url, {'email': 'testuser@example.com'})
    #     self.assertEqual(response.status_code, 200)
    #     response_data = response.json()
    #     self.assertEqual(response_data['status_code'], 1)
    #     self.assertEqual(response_data['message'], 'success')

    def test_reset_password_email_not_found(self):
        response = self.client.post(self.reset_password_url, {'email': 'nonexistent@example.com'})
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status_code'], 2)
        self.assertEqual(response_data['message'], 'email not found')

    def test_reset_password_form_invalid(self):
        response = self.client.post(self.reset_password_url, {'email': 'invalid'})
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status_code'], 4)

    # def test_reset_password_confirm_success(self):
    #     response = self.client.post(self.reset_password_confirm_url, {
    #         'new_password1': 'newpassword',
    #         'new_password2': 'newpassword'
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     response_data = response.json()
    #     self.assertEqual(response_data['status_code'], 1)
    #     self.assertEqual(response_data['message'], 'success')
    #     self.user.refresh_from_db()
    #     self.assertTrue(self.user.check_password('newpassword'))

    def test_reset_password_confirm_code_invalid(self):
        invalid_url = reverse('reset_password_confirm', args=['invalidcode'])
        response = self.client.post(invalid_url, {
            'new_password1': 'newpassword',
            'new_password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status_code'], 2)
        self.assertEqual(response_data['message'], 'not valid')

    def make_code(user):
        ConfirmCode.objects.filter(user=user).delete()

        code = hashcode(user.username, str(timezone.now()))  
        ConfirmCode.objects.create(user=user, code=code)
        return code

