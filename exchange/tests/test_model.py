from django.test import TestCase
from django.core.exceptions import ValidationError
from exchange.models import Currency, Exchange


class ModelTests(TestCase):
    def setUp(self):
        self.us_currency = Currency.objects.create(
            name="US dolar",
            short_name="USD",
            rss_url="https://www.ecb.europa.eu/rss/fxref-usd.html",
        )

    def test_currency_str(self):
        """Test string represetation of the curency"""
        self.assertEqual(
            str(self.us_currency),
            f"{self.us_currency.name} ({self.us_currency.short_name})",
        )

    def test_exchange_str(self):
        """Test string represetation of the exchange"""

        exchange = Exchange.objects.create(
            currency=self.us_currency, exchange_date="2019-10-04", rate="1.0925"
        )
        self.assertEqual(
            str(exchange),
            f"({exchange.exchange_date}): "
            f"EUR 1 = {self.us_currency.short_name} {exchange.rate}",
        )

    def test_uniqness_of_exchange(self):
        """Exchange have to be uniq in date for one currency"""
        exchange1 = Exchange.objects.create(
            currency=self.us_currency, exchange_date="2019-10-04", rate="1.0925"
        )
        exchange2 = Exchange(
            currency=self.us_currency, exchange_date="2019-10-04", rate="1.0925"
        )
        with self.assertRaises(ValidationError):
            exchange2.validate_unique()

