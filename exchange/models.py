import uuid
from django.db import models


class Currency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=3)
    rss_url = models.URLField(max_length=200)

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f"{self.name} ({self.short_name})"


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

