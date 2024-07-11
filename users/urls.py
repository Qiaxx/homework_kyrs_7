from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentsListAPIView, PaymentsCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("payments/", PaymentsListAPIView.as_view(), name="payments"),
    path("payments/create/", PaymentsCreateAPIView.as_view(), name="payments_create"),
]
