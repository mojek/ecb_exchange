from __future__ import absolute_import, unicode_literals
from celery.utils.log import get_task_logger
from celery import shared_task
from exchange.models import Currency, Exchange

from bs4 import BeautifulSoup
import urllib.request


@shared_task
def fetch_rss_data(currency_id):
    currency = Currency.objects.get(id=currency_id)
    print(currency.rss_url)
    source = urllib.request.urlopen(currency.rss_url).read()
    doc = BeautifulSoup(source, "lxml")
    for item in doc.findAll("item"):
        rate = item.find("cb:value").text
        date = item.find("dc:date").text.split("T")[0]
        exchange = Exchange.objects.create(
            currency=currency, exchange_date=date, rate=rate
        )
        print(exchange)
