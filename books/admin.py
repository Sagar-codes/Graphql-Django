from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Category)
class CatAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]

@admin.register(models.Quizzes) 
class QuizAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
    ]

class AnswerInlineModel(admin.TabularInline):
    model = models.Answers
    fields= [
        'answer_text',
        'is_right',
    ]

@admin.register(models.Questions)
class Questiondmin(admin.ModelAdmin):
    fields = [
        'title',
        'quiz',
    ]
    list_display = [
        'title',
        'quiz',
    ]
    inlines=[
        AnswerInlineModel
    ]


@admin.register(models.Answers)
class AnswerAdmin(admin.ModelAdmin):
        list_display = [
            'answer_text',
            'is_right',
            'question'
        ]
