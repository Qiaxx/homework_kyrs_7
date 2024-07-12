from rest_framework import viewsets
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer
from users.permissions import ModeratorPermission, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permission(self):
        if self.action in ["retrieve", "update", "partial_update"]:
            self.permission_classes = [ModeratorPermission | IsOwner,]
        elif self.action == "create":
            self.permission_classes = [~ModeratorPermission,]
        elif self.action == "destroy":
            self.permission_classes = [~ModeratorPermission & IsOwner, ]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
    permission_classes = [IsOwner, ]
