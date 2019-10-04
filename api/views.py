from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin
from .serializers import CurrencySerializer, ExchangeSerializer
from exchange.models import Currency, Exchange
from exchange.tasks import fetch_rss_data


class CurrencyViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    def perform_create(self, serializer):
        model_data = serializer.save()
        fetch_rss_data.delay(model_data.id)

    
class ExchangeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
