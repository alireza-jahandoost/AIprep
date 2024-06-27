from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


# Create your models here.

class QuestionType(models.Model):
    name = models.CharField(max_length=100)


class QuestionTypeData(models.Model):
    TYPE_TPO = 1
    TYPE_NEO = 2
    TYPE_CHOICES = [
        (TYPE_TPO, _("TPO")),
        (TYPE_NEO, _("NEO")),
    ]

    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    type_name = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, null=True, blank=True)
    type_number = models.PositiveIntegerField(null=True, blank=True)
    data = models.TextField()


class Correction(models.Model):
    question_type_data = models.ForeignKey(QuestionTypeData, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField(blank=True, null=True)
    correction = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
