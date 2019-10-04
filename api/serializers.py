from rest_framework import serializers
from exchange.models import Currency, Exchange


class CurrencySerializer(serializers.ModelSerializer):
    exchange_url = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name="exchange:exchanges-list",
        lookup_field="pk",
        lookup_url_kwarg="parent_lookup_currency",
    )

    class Meta:
        model = Currency
        fields = ("id", "name", "short_name", "rss_url", "exchange_url")
        read_only_field = ("id", "exchange_url")


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = ("id", "currency", "exchange_date", "rate")
        read_only_field = ("id", "currency")
