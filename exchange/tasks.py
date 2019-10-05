from __future__ import absolute_import, unicode_literals
from celery.utils.log import get_task_logger
from celery import shared_task
from exchange.models import Currency, Exchange



@shared_task
def fetch_rss_data(currency_id):
    currency = Currency.objects.get(id=currency_id)
    currency.fetch_rss_from_ecb()
    return currency
