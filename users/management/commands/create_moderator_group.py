from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from lms.models import Course, Lesson


class Command(BaseCommand):
    help = "Создание группы Модераторов с необходимыми правами"

    def handle(self, *args, **kwargs):
        # Создаем группу Модераторы
        moderators_group, created = Group.objects.get_or_create(name="Модераторы")

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модераторы" успешно создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модераторы" уже существует'))

        # Получение разрешений
        course_content_type = ContentType.objects.get_for_model(Course)
        lesson_content_type = ContentType.objects.get_for_model(Lesson)

        permissions = [
            Permission.objects.get(codename='view_course', content_type=course_content_type),
            Permission.objects.get(codename='change_course', content_type=course_content_type),
            Permission.objects.get(codename='view_lesson', content_type=lesson_content_type),
            Permission.objects.get(codename='change_lesson', content_type=lesson_content_type)
        ]

        for perm in permissions:
            moderators_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Разрешения добавлены к группе "Модераторы"'))
