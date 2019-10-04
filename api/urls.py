from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import CurrencyViewSet

router = DefaultRouter()
router.register("currency", CurrencyViewSet)

app_name = "exchange"
urlpatterns = [path("", include(router.urls))]
