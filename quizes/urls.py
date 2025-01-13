from django.urls import path
from quizes.views import *

urlpatterns = [
    path('<str:quiz_id>/create_question/', create_question, name='create_question'),
    path('<str:quiz_id>/<str:question_id>/edit_question/', edit_question, name='edit_question'),

    path('<str:quiz_id>/preview', preview_quiz, name='preview_quiz'),
    path('<str:quiz_id>/<str:question_id>/', quiz_question, name='quiz_question'),
    path('<str:quiz_id>/results/', quiz_results, name='quiz_results'),

    path('material/create', create_material, name="create_material"),
    path('material/<str:mat_id>/edit', edit_material, name="edit_material"),
    path('material/<str:mat_id>/delete', delete_material, name="delete_material"),
]
