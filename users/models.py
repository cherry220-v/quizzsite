from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from uuid import uuid4

from quizes.models import Quiz, Results

class User(AbstractUser):
    photo = models.ImageField(
        upload_to="users/avatars/",
        default="users/default.webp",
        blank=True,
        null=True,
        verbose_name="photo"
    )
    date_birth = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="birth_date"
    )
    completed_quizzes = models.ManyToManyField(
        Quiz,
        through=Results,
        related_name='completed_by',
        verbose_name="completed_quizzes"
    )
    email_activated = models.BooleanField(
        default=False
    )
    confirm_key = models.UUIDField(
        default=uuid4,
        verbose_name="confirm_key"
    )

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        verbose_name="groups",
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_query_name="user",
    )

    def __str__(self):
        return self.username
