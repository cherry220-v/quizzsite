from django.contrib import admin
from .models import Topic, Quiz, Question, Answer, Results

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'visibleId')                           # Поля списка
    search_fields = ('name', 'visibleId')                                # Поля для поиска
    readonly_fields = ('visibleId',)                                     # Только для чтения
    ordering = ('name',)                                                   # Сортировка

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'visibleId', 'topic', 'description')   # Поля списка
    search_fields = ('name', 'description', 'visibleId')                 # Поля для поиска
    list_filter = ('topic',)                                             # Фильтр по теме
    readonly_fields = ('visibleId',)                                     # Только для чтения
    ordering = ('name',)                                                   # Сортировка

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'id', 'visibleId', 'text')                   # Поля списка
    search_fields = ('text', 'visibleId')                                # Поля для поиска
    list_filter = ('quiz',)                                              # Фильтр по квизу
    readonly_fields = ('visibleId',)                                     # Только для чтения
    ordering = ('text',)                                                   # Сортировка

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'id', 'visibleId', 'text', 'isCorrect')  # Поля списка
    search_fields = ('text', 'visibleId')                                # Поля для поиска
    list_filter = ('isCorrect', 'question')                              # Фильтры
    readonly_fields = ('visibleId',)                                     # Только для чтения
    ordering = ('question',)

@admin.register(Results)
class ResultsAdmin(admin.ModelAdmin):
    list_display = ('id', 'visibleId', 'user', 'quiz', 'data')           # Поля списка
    search_fields = ('user__username', 'quiz__name', 'visibleId')        # Поля для поиска
    list_filter = ('quiz', 'user')                                       # Фильтры
    readonly_fields = ('visibleId',)                                     # Только для чтения
    ordering = ('quiz',)