from django.urls import path
from quizes.views import *

app_name = "quizes"

urlpatterns = [
    path('q/<str:quiz_id>/create_question/', create_question, name='create_question'),
    path('q/<str:quiz_id>/q/<str:question_id>/edit/', edit_question, name='edit_question'),
    path('q/<str:quiz_id>/q/<str:question_id>/delete/', delete_question, name='edit_question'),

    path('q/<str:quiz_id>', preview_quiz, name='preview_quiz'),
    path('q/<str:quiz_id>/results/', quiz_results, name='quiz_results'),
    path('q/<str:quiz_id>/start/', start_quiz, name='start_quiz'),
    path('q/<str:quiz_id>/q/<str:question_id>/', quiz_question, name='quiz_question'),
    path('q/<str:quiz_id>/completed/', quiz_results, name='quiz_completed'),

    path('', topic_search, name="search"),

    path('materials', materials_list, name="materials_list"),
    path('material/create', create_material, name="create_material"),
    path('material/<str:mat_id>/', edit_material, name="preview_material"),
    path('material/<str:mat_id>/edit', edit_material, name="edit_material"),
    path('material/<str:mat_id>/delete', delete_material, name="delete_material"),
]
