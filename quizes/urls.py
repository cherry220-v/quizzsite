from django.urls import path
from quizes.views import create_question

urlpatterns = [
    path('<int:quiz_id>/create_question/', create_question, name='create_question'),
]
