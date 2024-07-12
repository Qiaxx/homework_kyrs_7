from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer


class PaymentsListAPIView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date_payment']
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']


class PaymentsCreateAPIView(CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny,]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()