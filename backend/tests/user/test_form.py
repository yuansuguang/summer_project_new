from django.test import TestCase
from user.form import *

class FormsTestCase(TestCase):

    def test_register_form_valid(self):
        form_data = {
            'username': 'testuser',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
            'email': 'test@example.com'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_valid(self):
        form_data = {
            'username': 'testuser',
            'password': 'securepassword123'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_missing_username(self):
        form_data = {
            'username': '',
            'password': 'securepassword123'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_change_password_form_valid(self):
        form_data = {
            'old_password': 'oldpassword123',
            'new_password1': 'newsecurepassword123',
            'new_password2': 'newsecurepassword123'
        }
        form = ChangePasswordForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_reset_password_form_valid(self):
        form_data = {
            'email': 'test@example.com'
        }
        form = ResetPasswordForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_reset_password_form_invalid_missing_email(self):
        form_data = {
            'email': ''
        }
        form = ResetPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_set_password_form_valid(self):
        form_data = {
            'new_password1': 'newsecurepassword123',
            'new_password2': 'newsecurepassword123'
        }
        form = SetPasswordForm(data=form_data)
        self.assertTrue(form.is_valid())
