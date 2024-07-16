from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class LMSTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.course = Course.objects.create(
            title="Test course", description="test description course", user=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Test lesson",
            description="test description lesson",
            course=self.course,
            user=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_read_lesson(self):
        url = reverse("lms:lesson_retrieve", args=[self.lesson.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.lesson.title)

    def test_create_lesson(self):
        url = reverse("lms:lesson_create")
        response = self.client.post(url, self.lesson)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_update_lesson(self):
        url = reverse("lms:lesson_update", args=[self.lesson.pk])
        new_title = "New test lesson"
        response = self.client.put(url, {"title": new_title})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(pk=self.lesson.pk).title, new_title)

    def test_delete_lesson(self):
        url = reverse("lms:lesson_delete", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_subscribe_to_course(self):
        url = reverse("lms:subscription", args=[self.course.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 1)

    def test_unsubcribe_to_course(self):
        url = reverse("lms:subscription", args=[self.course.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 0)
