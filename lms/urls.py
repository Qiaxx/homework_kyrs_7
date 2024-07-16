from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import (CourseViewSet, LessonCreateAPIView,
                       LessonDestroyAPIView, LessonListAPIView,
                       LessonRetrieveAPIView, LessonUpdateAPIView,
                       SubscriptionToggleAPIView)

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="course")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path(
        "lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"
    ),
    path(
        "lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_delete"
    ),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path(
        "subscription/toggle/", SubscriptionToggleAPIView.as_view(), name="subscription"
    ),
] + router.urls
