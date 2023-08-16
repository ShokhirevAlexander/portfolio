import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from .models import EmailVerification


class RegistrationAndAuthenticationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('testpassword'))

    def test_email_verification_creation(self):
        verification = EmailVerification.objects.create(
            code='123e4567-e89b-12d3-a456-426655440000',
            user=self.user,
            expiration=datetime.datetime.now() + datetime.timedelta(days=1)
        )
        self.assertEqual(verification.code, '123e4567-e89b-12d3-a456-426655440000')
        self.assertEqual(verification.user, self.user)
        self.assertLessEqual(verification.expiration, datetime.datetime.now() + datetime.timedelta(days=1))

    def test_send_verification_email(self):
        verification = EmailVerification.objects.create(
            code='123e4567-e89b-12d3-a456-426655440000',
            user=self.user,
            expiration=datetime.datetime.now() + datetime.timedelta(days=1)
        )
        verification.send_verification_email()
        self.assertEqual(len(mail.outbox), 1)  # проверяем, что было отправлено одно письмо
        self.assertEqual(mail.outbox[0].subject,
                         f'Подверждение учетной записи для {self.user.username}')  # проверяем тему письма
        self.assertIn(self.user.email, mail.outbox[0].to)  # проверяем получателя письма
        self.assertIn(
            f'{reverse("users:email_verification", kwargs={"email": self.user.email, "code": verification.code})}',
            mail.outbox[0].body)  # проверяем содержимое письма

    def test_is_expired(self):
        expired_verification = EmailVerification.objects.create(
            code='123e4567-e89b-12d3-a456-426655440000',
            user=self.user,
            expiration=datetime.datetime.now() - datetime.timedelta(days=1)
        )
        self.assertTrue(expired_verification.is_expired())

        non_expired_verification = EmailVerification.objects.create(
            code='123e4567-e89b-12d3-a456-426655440000',
            user=self.user,
            expiration=datetime.datetime.now() + datetime.timedelta(days=1)
        )
        self.assertFalse(non_expired_verification.is_expired())