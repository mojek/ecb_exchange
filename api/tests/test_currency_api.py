from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.test.client import RequestFactory
from rest_framework.test import APIClient

from exchange.models import Currency
from api.serializers import CurrencySerializer

CURRENCY_URL = reverse("exchange:currency-list")


class PublicCurrencyApiTest(TestCase):
    """Test the publicity available currency api"""

    def setUp(self):
        self.client = APIClient()
        self.factory = RequestFactory()

    def test_retrive_currencies(self):
        Currency.objects.create(
            name="US dolar",
            short_name="USD",
            rss_url="https://www.ecb.europa.eu/rss/fxref-usd.html",
        )
        Currency.objects.create(
            name="Polish zloty",
            short_name="PLN",
            rss_url="https://www.ecb.europa.eu/rss/fxref-pln.html",
        )

        res = self.client.get(CURRENCY_URL)
        request = self.factory.get(CURRENCY_URL)
        currencies = Currency.objects.all().order_by("-name")
        serializer = CurrencySerializer(
            currencies, many=True, context={"request":request}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_currency_with_sucesss(self):
        """Test creating a new currency with invalid good payload"""
        payload = dict(
            name="Polish zloty",
            short_name="PLN",
            rss_url="https://www.ecb.europa.eu/rss/fxref-pln.html",
        )
        self.client.post(CURRENCY_URL, payload)
        exists = Currency.objects.filter(name=payload["name"]).exists()
        self.assertTrue(exists)

    def test_create_currency_invalid(self):
        """Test creating a new currency with invalid payload"""
        payload = {"name": ""}
        res = self.client.post(CURRENCY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
