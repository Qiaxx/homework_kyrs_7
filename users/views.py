from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView

from users.models import Payments
from users.serializers import PaymentsSerializer


class PaymentsListAPIView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date_payment']
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']


class PaymentsCreateAPIView(CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
