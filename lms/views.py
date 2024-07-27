from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import EMAIL_HOST_USER
from lms.models import Course, Lesson, Subscription
from lms.paginators import LmsPagination
from lms.serializers import (CourseDetailSerializer, CourseSerializer,
                             LessonSerializer)
from users.permissions import IsOwner, ModeratorPermission


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = LmsPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permission(self):
        if self.action in ["retrieve", "update", "partial_update"]:
            self.permission_classes = [
                ModeratorPermission | IsOwner,
            ]
        elif self.action == "create":
            self.permission_classes = [
                ~ModeratorPermission,
            ]
        elif self.action == "destroy":
            self.permission_classes = [
                ~ModeratorPermission & IsOwner,
            ]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=("put", "patch"))
    def update_course_and_notify_subscribers(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = self.get_serializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Получаем всех подписчиков курса
            subscriptions = Subscription.objects.filter(course=course)
            subscribers = [subscription.user for subscription in subscriptions]

            # Отправка уведомлений подписчикам
            for subscriber in subscribers:
                send_mail(
                    "Обновление курса",
                    f'Курс "{course.title}" был обновлен.',
                    EMAIL_HOST_USER,
                    [subscriber.email],
                    fail_silently=False,
                )

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~ModeratorPermission, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [ModeratorPermission, IsOwner]
    pagination_class = LmsPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [ModeratorPermission, IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [ModeratorPermission, IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsOwner,
    ]


class SubscriptionToggleAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, pk=course_id)

        subscription = Subscription.objects.filter(user=user, course=course_item)
        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message})
