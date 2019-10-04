from rest_framework import serializers
from exchange.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "name", "short_name", "rss_url")
