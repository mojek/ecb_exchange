from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from exchange.models import Exchange, Currency
from api.serializers import ExchangeSerializer


class PublicExchangeApiTest(TestCase):
    """Test the publicity available exchange api"""

    def setUp(self):
        self.client = APIClient()

    def test_retrive_exchange(self):
        currency_us = Currency.objects.create(
            name="US dolar",
            short_name="USD",
            rss_url="https://www.ecb.europa.eu/rss/fxref-usd.html",
        )

        currency_pl = Currency.objects.create(
            name="Polish zloty",
            short_name="PLN",
            rss_url="https://www.ecb.europa.eu/rss/fxref-pln.html",
        )

        exchange1 = Exchange.objects.create(
            currency=currency_us, exchange_date="2019-10-01", rate="1.0925"
        )
        exchange2 = Exchange.objects.create(
            currency=currency_us, exchange_date="2019-10-02", rate="2.0925"
        )
        exchange3 = Exchange.objects.create(
            currency=currency_pl, exchange_date="2019-10-03", rate="3.0925"
        )

        r_url = reverse("exchange:exchanges-list", args=[currency_us.id])
        res = self.client.get(r_url)
        serializer = ExchangeSerializer(currency_us.exchanges.all(), many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
