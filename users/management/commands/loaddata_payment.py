from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from lms.models import Course, Lesson
from users.models import Payments


class Command(BaseCommand):
    help = 'Загружает данные платежей'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        course1 = Course.objects.get(pk=1)
        lesson1 = Lesson.objects.get(pk=1)

        payments = [
            {
                'user': user1,
                'date_payment': datetime(2024, 7, 8, 12, 0),
                'paid_course': course1,
                'paid_lesson': None,
                'amount': 100.00,
                'payment_method': 'cash'
            },
            {
                'user': user2,
                'date_payment': datetime(2024, 7, 9, 12, 0),
                'paid_course': None,
                'paid_lesson': lesson1,
                'amount': 50.00,
                'payment_method': 'bank_transfer'
            }
        ]

        for payment_data in payments:
            Payments.objects.create(**payment_data)

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены'))