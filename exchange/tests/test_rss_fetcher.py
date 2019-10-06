from django.test import TestCase
from exchange.tasks import fetch_rss_data
from exchange.models import Currency


class FetcherRssTest(TestCase):
    def test_fetch_rss_data_success(self):
        """Test Fetch data from rss and update last_fetch"""
        currency = Currency.objects.create(
            name="US dolar",
            short_name="USD",
            rss_url="https://www.ecb.europa.eu/rss/fxref-usd.html",
        )
        fetch_rss_data(currency.id)
        currency.refresh_from_db()
        self.assertIsNotNone(currency.last_fetch)

    def test_fetch_rss_data_fails(self):
        """Test Fetch data from rss with wrong url"""
        currency = Currency.objects.create(
            name="US dolar", short_name="USD", rss_url="http://mojek_wrong_domain.com"
        )
        fetch_rss_data(currency.id)
        currency.refresh_from_db()
        self.assertIsNone(currency.last_fetch)
