from django.contrib import admin

from materials.models import Section, Lesson, Examination, Answer, Question, Choice


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "description", "img")
    search_fields = ("name", "description")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "section", "name", "description", "img")
    search_fields = ("name", "description")


@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "lesson")
    search_fields = ("name",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "examination", "text")
    search_fields = ("text",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "question", "choice", "created")
    search_fields = ("question",)
