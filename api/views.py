from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin
from .serializers import CurrencySerializer, ExchangeSerializer
from exchange.models import Currency, Exchange


class CurrencyViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ExchangeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
