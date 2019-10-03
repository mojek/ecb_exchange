from django.test import TestCase

from exchange.models import Currency, Exchange


class ModelTests(TestCase):
    def test_currency_str(self):
        """Test string represetation of the curency"""
        currency = Currency.objects.create(
            name="US dolar",
            short_name="USD",
            rss_url="https://www.ecb.europa.eu/rss/fxref-usd.html",
        )
        self.assertEqual(str(currency), f"{currency.name} ({currency.short_name})")

    def test_exchange_str(self):
        """Test string represetation of the exchange"""
        currency = Currency.objects.create(
            name="US dolar",
            short_name="USD",
            rss_url="https://www.ecb.europa.eu/rss/fxref-usd.html",
        )
        exchange = Exchange.objects.create(
            currency=currency, exchange_date="2019-10-04", rate="1.0925"
        )
        self.assertEqual(
            str(exchange),
            f"({exchange.exchange_date}): "
            f"EUR 1 = {currency.short_name} {exchange.rate}",
        )
