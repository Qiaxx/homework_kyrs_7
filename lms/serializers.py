from rest_framework.serializers import ModelSerializer, SerializerMethodField, URLField

from lms.models import Course, Lesson, Subscription
from lms.validators import validate_lesson_url


class LessonSerializer(ModelSerializer):
    video_url = URLField(validators=[validate_lesson_url])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = SerializerMethodField()

    def get_lesson_count(self, course):
        return course.lessons.count()

    def get_is_subscribed(self, course):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user, course=course
            ).exists()
        return False

    class Meta:
        model = Course
        fields = ("title", "description", "lesson_count", "lessons")


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
