from rest_framework.serializers import ValidationError


def validate_lesson_url(value):
    if not value.endswith("youtube.com"):
        raise ValidationError(
            "Ссылка на видео должна относится исключительно к сервису youtube"
        )
