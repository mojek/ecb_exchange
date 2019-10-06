import uuid
import datetime
from django.db import models
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import URLError
from django.core.exceptions import ValidationError


class Currency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=3)
    rss_url = models.URLField(max_length=200)
    last_fetch = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f"{self.name} ({self.short_name})"

    def fetch_rss_from_ecb(self):
        try:
            source = urllib.request.urlopen(self.rss_url).read()
        except URLError:
            return None
        else:
            doc = BeautifulSoup(source, "lxml")
            for item in doc.findAll("item"):
                rate = item.find("cb:value").text
                date = item.find("dc:date").text.split("T")[0]
                exchange = Exchange(currency=self, exchange_date=date, rate=rate)
                try:
                    exchange.full_clean()
                except ValidationError:
                    continue
                else:
                    exchange.save()
            self.last_fetch = datetime.date.today()
            self.save()


class Exchange(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="exchanges"
    )
    exchange_date = models.DateField()
    rate = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        unique_together = ["currency", "exchange_date"]

    def __str__(self):
        return f"({self.exchange_date}): EUR 1 = {self.currency.short_name} {self.rate}"

