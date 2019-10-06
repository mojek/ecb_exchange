from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from exchange.models import Exchange, Currency
from api.serializers import ExchangeSerializer

from django.conf import settings

settings.CELERY_TASK_ALWAYS_EAGER = True


class PublicExchangeApiTest(TestCase):
    def test_(self):
        self.currency_us = Currency.objects.create(
            name="US dolar",
            short_name="USD",
            rss_url="https://www.ecb.europa.eu/rss/fxref-usd.html",
        )
        payload = dict(
            currency=self.currency_us.id, exchange_date="2019-10-01", rate="1.0922"
        )
        r_url = reverse("exchange:exchanges-list", args=[self.currency_us.id])
        res = self.client.post(r_url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateExchangeApiTest(TestCase):
    """Test the private available exchange api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user("test@mojek.pl", "pass123")
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.currency_us = Currency.objects.create(
            name="US dolar",
            short_name="USD",
            rss_url="https://www.ecb.europa.eu/rss/fxref-usd.html",
        )

        self.currency_pl = Currency.objects.create(
            name="Polish zloty",
            short_name="PLN",
            rss_url="https://www.ecb.europa.eu/rss/fxref-pln.html",
        )

    def test_retrive_exchange(self):
        exchange1 = Exchange.objects.create(
            currency=self.currency_us, exchange_date="2019-10-01", rate="1.0925"
        )
        exchange2 = Exchange.objects.create(
            currency=self.currency_us, exchange_date="2019-10-02", rate="2.0925"
        )
        exchange3 = Exchange.objects.create(
            currency=self.currency_pl, exchange_date="2019-10-03", rate="3.0925"
        )

        r_url = reverse("exchange:exchanges-list", args=[self.currency_us.id])
        res = self.client.get(r_url)
        serializer = ExchangeSerializer(self.currency_us.exchanges.all(), many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_save_exchange(self):
        """Send exchange payload to save with success"""
        payload = dict(
            currency=self.currency_us.id, exchange_date="2019-10-01", rate="1.0922"
        )
        r_url = reverse("exchange:exchanges-list", args=[self.currency_us.id])
        self.client.post(r_url, payload)
        exists = self.currency_us.exchanges.filter(
            exchange_date=payload["exchange_date"]
        ).exists()
        self.assertTrue(exists)

    def test_post_same_exchange_with_fail(self):
        """Test send exchange to the currency with same date fail to"""
        payload = dict(
            currency=self.currency_us.id, exchange_date="2019-10-01", rate="1.0921"
        )
        r_url = reverse("exchange:exchanges-list", args=[self.currency_us.id])
        res1 = self.client.post(r_url, payload)
        res2 = self.client.post(r_url, payload)
        exchanges = self.currency_us.exchanges.all()
        self.assertEqual(len(exchanges), 1)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
