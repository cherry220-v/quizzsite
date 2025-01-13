from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
import uuid

class Topic(models.Model):
    id = models.AutoField(
        verbose_name="id",
        editable=False,
        primary_key=True
    )
    visibleId = models.UUIDField(
        verbose_name="visibleId",
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(
        verbose_name="name",
        max_length=25,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name

class Quiz(models.Model):
    id = models.AutoField(
        verbose_name="id",
        editable=False,
        primary_key=True,
    )
    visibleId = models.UUIDField(
        verbose_name="visibleId",
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    topic = models.ForeignKey(
        Topic,
        related_name='quizzes',
        verbose_name="topic",
        on_delete=models.CASCADE
    )

    name = models.CharField(
        verbose_name="name",
        max_length=50,
        null=False,
        blank=False,
    )

    description = models.CharField(
        verbose_name="description",
        max_length=180,
        null=False,
        blank=False,
    )

    author = models.ForeignKey(
        "users.User",
        related_name='created_quizzes',
        verbose_name="author",
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        verbose_name="image",
        blank=True,
        null=True,
        upload_to='quizes/'
    )

    def __str__(self):
        return self.name

class Question(models.Model):
    id = models.AutoField(
        verbose_name="id",
        editable=False,
        primary_key=True
    )
    visibleId = models.UUIDField(
        verbose_name="visibleId",
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    quiz = models.ForeignKey(
        Quiz,
        verbose_name="quiz",
        related_name='questions',
        on_delete=models.CASCADE
    )
    text = models.CharField(
        verbose_name="text",
        max_length=1275,
        null=False,
        blank=False,
    )

    image = models.ImageField(
        verbose_name="image",
        blank=True,
        null=True,
        upload_to='questions/'
    )

    def __str__(self):
        return self.text

class Answer(models.Model):
    id = models.AutoField(
        verbose_name="id",
        editable=False,
        primary_key=True
    )
    visibleId = models.UUIDField(
        verbose_name="visibleId",
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE
    )

    text = models.CharField(
        verbose_name="text",
        max_length=275,
        null=False,
        blank=False,
    )

    image = models.ImageField(
        verbose_name="image",
        blank=True,
        null=True,
        upload_to='answers/',
    )

    isCorrect = models.BooleanField(
        verbose_name="isCorrect",
        blank=False,
        null=False,
        default=False,
    )

    def __str__(self):
        return self.text

    def customClean(self):
        if self.isCorrect and Answer.objects.filter(question=self.question, isCorrect=True).exists():
            raise ValidationError("У вопроса уже есть правильный ответ.")

class Results(models.Model):
    id = models.AutoField(
        verbose_name="id",
        editable=False,
        primary_key=True
    )
    visibleId = models.UUIDField(
        verbose_name="visibleId",
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    user = models.ForeignKey(
        "users.User",
        verbose_name="user",
        on_delete=models.CASCADE
    )
    quiz = models.ForeignKey(
        Quiz,
        related_name='results',
        on_delete=models.CASCADE
    )
    data = models.JSONField(
        verbose_name="data",
        default=dict,
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'quiz'], name='unique_user_quiz')
        ]
