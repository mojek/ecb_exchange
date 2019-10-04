from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin


from .views import CurrencyViewSet, ExchangeViewSet


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


router = NestedDefaultRouter()
(
    router.register("currencies", CurrencyViewSet).register(
        "exchanges",
        ExchangeViewSet,
        basename="exchanges",
        parents_query_lookups=["currency"],
    )
)


app_name = "exchange"
urlpatterns = [path("", include(router.urls))]
