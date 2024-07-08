from django.contrib import admin

from lms.models import Course, Lesson


@admin.register(Lesson)
class LessonInline(admin.ModelAdmin):
    model = Lesson
    list_display = (
        "title",
        "description",
        "course",
    )
    list_filter = ("title", "course")
    search_fields = ("title", "course")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ("title", "description")
    list_filter = ("title",)
    search_fields = ("title",)
